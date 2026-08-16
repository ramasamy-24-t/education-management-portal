"""AI Engine features. Always persist something useful; model failures use local fallbacks."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session, joinedload

from app.models.ai_insight import AIInsight, InsightType
from app.models.assignment import AssignmentSubmission
from app.models.attendance import Attendance, AttendanceStatus
from app.models.course import ClassGroup
from app.models.exam import Exam, ExamAnalysis, Grade
from app.models.user import User, UserRole
from app.services import ai_service
from app.services.academic_access import enrolled_students, list_accessible_classes

AT_RISK_ATTENDANCE = 70.0
AT_RISK_EXAM = 60.0
STALE_AFTER = timedelta(hours=6)
# Seed attendance is 5 consecutive days; 2-week windows would always be empty.
TREND_WINDOW_DAYS = 3
TREND_VALUES = ("improving", "worsening", "stable")
NOT_ENOUGH_DATA = "Not enough data yet"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _latest(db: Session, *, student_id: int | None, class_id: int | None, insight_type: InsightType) -> AIInsight | None:
    query = db.query(AIInsight).filter(AIInsight.type == insight_type)
    if student_id is None:
        query = query.filter(AIInsight.student_id.is_(None))
    else:
        query = query.filter(AIInsight.student_id == student_id)
    if class_id is None:
        query = query.filter(AIInsight.class_id.is_(None))
    else:
        query = query.filter(AIInsight.class_id == class_id)
    return query.order_by(AIInsight.created_at.desc()).first()


def _upsert(
    db: Session,
    *,
    student_id: int | None,
    class_id: int | None,
    insight_type: InsightType,
    content: str,
    trend: str | None = None,
    trend_reason: str | None = None,
) -> AIInsight:
    row = _latest(db, student_id=student_id, class_id=class_id, insight_type=insight_type)
    if row:
        row.content = content
        row.created_at = _now()
        if insight_type == InsightType.at_risk:
            row.trend = trend
            row.trend_reason = trend_reason
        return row
    row = AIInsight(
        student_id=student_id,
        class_id=class_id,
        type=insight_type,
        content=content,
        trend=trend if insight_type == InsightType.at_risk else None,
        trend_reason=trend_reason if insight_type == InsightType.at_risk else None,
    )
    db.add(row)
    return row


def _is_fresh(row: AIInsight | None) -> bool:
    if row is None or not row.content:
        return False
    created = row.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    return _now() - created < STALE_AFTER


def student_snapshot(db: Session, student: User) -> dict:
    from app.services.assignments import list_assignments, my_submissions
    from app.services.attendance import attendance_summary
    from app.services.exams import my_grade_history

    classes = list_accessible_classes(db, student)
    summaries = []
    for class_group in classes:
        summaries.extend(attendance_summary(db, student, class_id=class_group.id))
    attendance_percent = (
        round(sum(item.percent_present for item in summaries) / len(summaries), 1) if summaries else 0.0
    )
    grades = my_grade_history(db, student)
    exam_avg = round(sum(item.percent for item in grades) / len(grades), 1) if grades else 0.0
    assignments = list_assignments(db, student)
    submissions = my_submissions(db, student)
    return {
        "student_id": student.id,
        "name": student.name,
        "attendance_percent": attendance_percent,
        "exam_average": exam_avg,
        "course_titles": sorted({item.course_title for item in grades if item.course_title}),
        "grade_lines": [
            f"{item.course_title} / {item.exam_title}: {item.marks_obtained}/{item.max_marks} ({item.percent}%)"
            for item in grades
        ],
        "attendance_lines": [f"{item.class_name}: {item.percent_present}%" for item in summaries],
        "assignments_submitted": len({row.assignment_id for row in submissions}),
        "assignments_total": len(assignments),
        "at_risk": attendance_percent < AT_RISK_ATTENDANCE or exam_avg < AT_RISK_EXAM,
    }


def _attendance_percent(rows: list[Attendance]) -> float | None:
    if not rows:
        return None
    present = sum(1 for row in rows if row.status in (AttendanceStatus.present, AttendanceStatus.late))
    return round((present / len(rows)) * 100, 1)


def _exam_average(rows: list[Grade]) -> float | None:
    percents = []
    for row in rows:
        max_marks = row.exam.max_marks if row.exam else 0
        if max_marks:
            percents.append((row.marks_obtained / max_marks) * 100)
    if not percents:
        return None
    return round(sum(percents) / len(percents), 1)


def student_trend_windows(db: Session, student: User) -> dict:
    """Two calendar windows of TREND_WINDOW_DAYS each, ending today."""
    today = date.today()
    recent_start = today - timedelta(days=TREND_WINDOW_DAYS)
    prior_start = today - timedelta(days=TREND_WINDOW_DAYS * 2)

    att_recent = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student.id,
            Attendance.date >= recent_start,
            Attendance.date <= today,
        )
        .all()
    )
    att_prior = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student.id,
            Attendance.date >= prior_start,
            Attendance.date < recent_start,
        )
        .all()
    )
    grades_recent = (
        db.query(Grade)
        .join(Exam)
        .options(joinedload(Grade.exam))
        .filter(Grade.student_id == student.id, Exam.date >= recent_start, Exam.date <= today)
        .all()
    )
    grades_prior = (
        db.query(Grade)
        .join(Exam)
        .options(joinedload(Grade.exam))
        .filter(Grade.student_id == student.id, Exam.date >= prior_start, Exam.date < recent_start)
        .all()
    )
    recent = {
        "attendance": _attendance_percent(att_recent),
        "exam_avg": _exam_average(grades_recent),
        "attendance_n": len(att_recent),
        "exam_n": len(grades_recent),
    }
    prior = {
        "attendance": _attendance_percent(att_prior),
        "exam_avg": _exam_average(grades_prior),
        "attendance_n": len(att_prior),
        "exam_n": len(grades_prior),
    }
    enough = recent["attendance_n"] > 0 and prior["attendance_n"] > 0
    return {
        "enough": enough,
        "recent": recent,
        "prior": prior,
        "recent_label": f"{recent_start.isoformat()} to {today.isoformat()}",
        "prior_label": f"{prior_start.isoformat()} to {(recent_start - timedelta(days=1)).isoformat()}",
    }


def _rule_trend(windows: dict) -> tuple[str, str]:
    recent, prior = windows["recent"], windows["prior"]
    parts = []
    score = 0.0
    if recent["attendance"] is not None and prior["attendance"] is not None:
        delta = recent["attendance"] - prior["attendance"]
        score += delta
        parts.append(f"attendance {prior['attendance']}% → {recent['attendance']}%")
    if recent["exam_avg"] is not None and prior["exam_avg"] is not None:
        delta = recent["exam_avg"] - prior["exam_avg"]
        score += delta
        parts.append(f"exam average {prior['exam_avg']}% → {recent['exam_avg']}%")
    detail = "; ".join(parts) if parts else "attendance moved little across the two windows"
    if score > 5:
        return "improving", f"Improving: {detail}."
    if score < -5:
        return "worsening", f"Worsening: {detail}."
    return "stable", f"Stable: {detail}."


def assess_risk_trend(db: Session, student: User) -> tuple[str | None, str]:
    """Return (trend, one-line reason). trend is None when there are not two windows."""
    windows = student_trend_windows(db, student)
    if not windows["enough"]:
        return None, NOT_ENOUGH_DATA

    parsed = ai_service.complete_json(
        "Compare two short academic windows for this student and return JSON with keys "
        "trend (exactly one of: improving, worsening, stable) and reason (one sentence).\n"
        f"Name: {student.name}\n"
        f"Recent window ({windows['recent_label']}): attendance={windows['recent']['attendance']}% "
        f"({windows['recent']['attendance_n']} records), exam_avg={windows['recent']['exam_avg']} "
        f"({windows['recent']['exam_n']} exams).\n"
        f"Prior window ({windows['prior_label']}): attendance={windows['prior']['attendance']}% "
        f"({windows['prior']['attendance_n']} records), exam_avg={windows['prior']['exam_avg']} "
        f"({windows['prior']['exam_n']} exams).\n"
        "If a metric is null, ignore it. Do not invent data."
    )
    if isinstance(parsed, dict):
        trend = str(parsed.get("trend") or "").strip().lower()
        reason = str(parsed.get("reason") or "").strip()
        if trend in TREND_VALUES and reason:
            return trend, reason
    return _rule_trend(windows)


def generate_assignment_feedback(db: Session, submission: AssignmentSubmission) -> str | None:
    assignment = submission.assignment
    prompt = (
        "You are a supportive teaching assistant. Write 2-3 sentences of constructive AI feedback "
        "for this graded student submission. Do not change the teacher's grade.\n"
        f"Assignment: {assignment.title if assignment else 'Assignment'}\n"
        f"Description: {assignment.description if assignment else ''}\n"
        f"Student work: {submission.content[:1500]}\n"
        f"Teacher grade: {submission.grade}\n"
        f"Teacher feedback: {submission.feedback}\n"
    )
    text = ai_service.complete(prompt, max_output_tokens=220)
    if not text:
        text = (
            f"Automated note: the teacher scored this {submission.grade}/100. "
            "Revise the weakest section mentioned in the teacher feedback and resubmit next time if allowed."
        )
    submission.ai_feedback = text
    db.add(submission)
    db.commit()
    return text


def generate_exam_analyses(db: Session, exam: Exam, grades: list[Grade]) -> None:
    class_group = exam.class_group
    course_title = class_group.course.title if class_group and class_group.course else "the course"
    lines = []
    for grade in grades:
        name = grade.student.name if grade.student else str(grade.student_id)
        percent = round((grade.marks_obtained / exam.max_marks) * 100, 1) if exam.max_marks else 0
        lines.append(f"{grade.student_id}|{name}|{grade.marks_obtained}/{exam.max_marks}|{percent}%")

    parsed = ai_service.complete_json(
        "Create a short exam analysis per student. Return a JSON array of objects with keys "
        "student_id (int), ai_summary (string), weak_topics (semicolon-separated string).\n"
        f"Exam: {exam.title} in {course_title}, max {exam.max_marks}.\n"
        "Rows: " + "; ".join(lines)
    )
    by_id: dict[int, dict] = {}
    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict) and item.get("student_id") is not None:
                by_id[int(item["student_id"])] = item

    for grade in grades:
        item = by_id.get(grade.student_id, {})
        percent = round((grade.marks_obtained / exam.max_marks) * 100, 1) if exam.max_marks else 0
        name = grade.student.name if grade.student else "Student"
        summary = item.get("ai_summary") or (
            f"{name} scored {grade.marks_obtained}/{exam.max_marks} ({percent}%) on {exam.title}."
        )
        weak = item.get("weak_topics") or (
            f"Review core topics in {course_title}" if percent < 70 else f"Minor gaps in {course_title}"
        )
        existing = (
            db.query(ExamAnalysis)
            .filter(ExamAnalysis.exam_id == exam.id, ExamAnalysis.student_id == grade.student_id)
            .first()
        )
        if existing:
            existing.ai_summary = str(summary)
            existing.weak_topics = str(weak)
        else:
            db.add(
                ExamAnalysis(
                    student_id=grade.student_id,
                    exam_id=exam.id,
                    ai_summary=str(summary),
                    weak_topics=str(weak),
                )
            )
    db.commit()


def refresh_student_insights(db: Session, student: User, *, force: bool = False) -> dict[str, str]:
    existing = {
        insight_type: _latest(db, student_id=student.id, class_id=None, insight_type=insight_type)
        for insight_type in (
            InsightType.performance,
            InsightType.at_risk,
            InsightType.weak_subject,
            InsightType.recommendation,
        )
    }
    if not force and all(_is_fresh(row) for row in existing.values() if row is not None) and existing[InsightType.performance]:
        at_risk_row = existing[InsightType.at_risk]
        if at_risk_row is not None and at_risk_row.trend is None and not at_risk_row.trend_reason:
            trend, trend_reason = assess_risk_trend(db, student)
            at_risk_row.trend = trend
            at_risk_row.trend_reason = trend_reason
            db.commit()
        return {key.value: (row.content if row else "") for key, row in existing.items()}

    snap = student_snapshot(db, student)
    trend, trend_reason = assess_risk_trend(db, student)
    parsed = ai_service.complete_json(
        "Analyze this student's academic record. Return JSON with keys: "
        "performance (string narrative), at_risk (boolean), at_risk_reason (string), "
        "weak_subjects (array of strings), recommendations (array of 3 short strings).\n"
        f"Name: {snap['name']}\n"
        f"Attendance: {snap['attendance_percent']}%\n"
        f"Exam average: {snap['exam_average']}%\n"
        f"Assignments: {snap['assignments_submitted']}/{snap['assignments_total']}\n"
        f"Grades: {snap['grade_lines']}\n"
        f"Attendance by class: {snap['attendance_lines']}\n"
        f"Rule-based at-risk flag: {snap['at_risk']}"
    )
    if not isinstance(parsed, dict):
        parsed = {}

    performance = parsed.get("performance") or (
        f"{snap['name']} has {snap['attendance_percent']}% attendance and a {snap['exam_average']}% exam average, "
        f"with {snap['assignments_submitted']}/{snap['assignments_total']} assignments submitted."
    )
    at_risk = bool(parsed.get("at_risk", snap["at_risk"]))
    at_risk_reason = parsed.get("at_risk_reason") or (
        "Attendance below 70% or exam average below 60%."
        if snap["at_risk"]
        else "Not currently flagged as at-risk."
    )
    weak = parsed.get("weak_subjects")
    if not weak:
        weak = []
        for line in snap["grade_lines"]:
            try:
                percent = float(line.rsplit("(", 1)[-1].rstrip("%)"))
            except (ValueError, IndexError):
                continue
            if percent < 70:
                weak.append(line.split(":")[0].strip())
        if not weak:
            weak = (
                ["No weak subjects flagged from current grades"]
                if snap["exam_average"] >= 70
                else ["Core exam topics"]
            )
    if isinstance(weak, str):
        weak = [weak]
    recs = parsed.get("recommendations") or [
        "Review the lowest-scoring exam first.",
        "Keep attendance above 80% this week.",
        "Finish any open assignments before the next due date.",
    ]
    if isinstance(recs, str):
        recs = [recs]

    _upsert(db, student_id=student.id, class_id=None, insight_type=InsightType.performance, content=str(performance))
    _upsert(
        db,
        student_id=student.id,
        class_id=None,
        insight_type=InsightType.at_risk,
        content=str(at_risk_reason) if at_risk else "Not currently flagged as at-risk.",
        trend=trend,
        trend_reason=trend_reason,
    )
    _upsert(db, student_id=student.id, class_id=None, insight_type=InsightType.weak_subject, content="; ".join(str(item) for item in weak))
    _upsert(db, student_id=student.id, class_id=None, insight_type=InsightType.recommendation, content=" | ".join(str(item) for item in recs))
    db.commit()
    return {
        "performance": str(performance),
        "at_risk": str(at_risk_reason) if at_risk else "Not currently flagged as at-risk.",
        "weak_subject": "; ".join(str(item) for item in weak),
        "recommendation": " | ".join(str(item) for item in recs),
        "trend": trend,
        "trend_reason": trend_reason,
    }


def refresh_class_insight(db: Session, class_group: ClassGroup, *, force: bool = False) -> str:
    existing = _latest(db, student_id=None, class_id=class_group.id, insight_type=InsightType.class_insight)
    if not force and _is_fresh(existing):
        return existing.content

    students = enrolled_students(db, class_group)
    snapshots = [student_snapshot(db, student) for student in students]
    flagged = [item for item in snapshots if item["at_risk"]]
    parsed = ai_service.complete_json(
        "Write a class-level teaching insight. Return JSON with keys: "
        "class_summary (string), at_risk (array of {student_id, reason}).\n"
        f"Class: {class_group.name} / {class_group.course.title if class_group.course else ''}\n"
        f"Students: {[{'id': s['student_id'], 'name': s['name'], 'attendance': s['attendance_percent'], 'exam_avg': s['exam_average']} for s in snapshots]}"
    )
    if not isinstance(parsed, dict):
        parsed = {}
    summary = parsed.get("class_summary") or (
        f"{class_group.name}: {len(students)} students, {len(flagged)} at-risk "
        f"(attendance < {AT_RISK_ATTENDANCE}% or exam average < {AT_RISK_EXAM}%)."
    )
    _upsert(db, student_id=None, class_id=class_group.id, insight_type=InsightType.class_insight, content=str(summary))

    reasons = {}
    if isinstance(parsed.get("at_risk"), list):
        for item in parsed["at_risk"]:
            if isinstance(item, dict) and item.get("student_id") is not None:
                reasons[int(item["student_id"])] = str(item.get("reason") or "Flagged by the model.")
    for snap in flagged:
        reason = reasons.get(snap["student_id"]) or (
            f"{snap['name']}: attendance {snap['attendance_percent']}%, exam average {snap['exam_average']}%."
        )
        student = next((item for item in students if item.id == snap["student_id"]), None)
        trend, trend_reason = assess_risk_trend(db, student) if student else (None, NOT_ENOUGH_DATA)
        _upsert(
            db,
            student_id=snap["student_id"],
            class_id=class_group.id,
            insight_type=InsightType.at_risk,
            content=reason,
            trend=trend,
            trend_reason=trend_reason,
        )
    db.commit()
    return str(summary)


def list_student_insight_texts(db: Session, student: User, *, refresh: bool = True) -> dict[str, list[str]]:
    if refresh:
        refresh_student_insights(db, student, force=False)
    rows = (
        db.query(AIInsight)
        .filter(AIInsight.student_id == student.id)
        .order_by(AIInsight.created_at.desc())
        .all()
    )
    weak = []
    tips = []
    insights = []
    recs = []
    at_risk_row = None
    for row in rows:
        if row.type == InsightType.weak_subject:
            weak.extend([part.strip() for part in row.content.split(";") if part.strip()])
        elif row.type == InsightType.recommendation:
            tips.extend([part.strip() for part in row.content.split("|") if part.strip()])
            recs.extend([part.strip() for part in row.content.split("|") if part.strip()])
        elif row.type in (InsightType.performance, InsightType.at_risk):
            insights.append(row.content)
        if row.type == InsightType.at_risk and at_risk_row is None:
            at_risk_row = row
        elif row.type == InsightType.at_risk and row.class_id is None:
            at_risk_row = row
    return {
        "weak_subjects": _unique(weak),
        "improvement_tips": _unique(tips),
        "ai_insights": _unique(insights),
        "ai_recommendations": _unique(recs),
        "risk_trend": at_risk_row.trend if at_risk_row else None,
        "risk_trend_reason": at_risk_row.trend_reason if at_risk_row else None,
    }


def list_monitoring(db: Session, actor: User) -> list[dict]:
    query = (
        db.query(AIInsight)
        .options(joinedload(AIInsight.student), joinedload(AIInsight.class_group))
        .order_by(AIInsight.created_at.desc())
    )
    if actor.role == UserRole.teacher:
        class_ids = [item.id for item in list_accessible_classes(db, actor)]
        if not class_ids:
            return []
        query = query.filter(AIInsight.class_id.in_(class_ids))
    elif actor.role != UserRole.admin:
        query = query.filter(AIInsight.student_id == actor.id)
    rows = query.limit(80).all()
    return [
        {
            "id": row.id,
            "student_id": row.student_id,
            "student_name": row.student.name if row.student else None,
            "class_id": row.class_id,
            "class_name": row.class_group.name if row.class_group else None,
            "type": row.type.value,
            "content": row.content,
            "trend": row.trend,
            "trend_reason": row.trend_reason,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]


def refresh_monitoring(db: Session, actor: User) -> int:
    classes = list_accessible_classes(db, actor)
    for class_group in classes:
        refresh_class_insight(db, class_group, force=True)
    return len(classes)


def generate_practice_questions(db: Session, student: User, subject: str) -> dict:
    """Fresh 3–4 questions each call. Not stored — regenerate on click."""
    cleaned = (subject or "").strip()
    if not cleaned:
        return {"subject": "", "questions": [], "source": "error", "detail": "Pick a weak subject first."}

    topics = [
        row.weak_topics.strip()
        for row in db.query(ExamAnalysis).filter(ExamAnalysis.student_id == student.id).all()
        if row.weak_topics and row.weak_topics.strip()
    ]
    topic_text = "; ".join(topics) if topics else "none recorded"

    parsed = ai_service.complete_json(
        "Write 4 short practice questions for a student who is weak in this subject. "
        "No answers. Return JSON with key questions (array of 3 or 4 strings).\n"
        f"Subject: {cleaned}\n"
        f"Exam analysis weak topics: {topic_text}"
    )
    questions: list[str] = []
    if isinstance(parsed, dict) and isinstance(parsed.get("questions"), list):
        questions = [str(item).strip() for item in parsed["questions"] if str(item).strip()]
    elif isinstance(parsed, list):
        questions = [str(item).strip() for item in parsed if str(item).strip()]
    questions = questions[:4]
    if len(questions) >= 3:
        return {"subject": cleaned, "questions": questions, "source": "model"}

    fallback = [
        f"Explain the core idea of {cleaned} in two sentences.",
        f"Work one short example using: {topics[0] if topics else cleaned}.",
        f"Name two common mistakes in {cleaned} and how to avoid them.",
        f"Write a 5-minute drill question on {cleaned}.",
    ]
    return {
        "subject": cleaned,
        "questions": fallback,
        "source": "fallback",
        "detail": "AI was unavailable, so these are local practice prompts. Retry for model-generated questions.",
    }


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
