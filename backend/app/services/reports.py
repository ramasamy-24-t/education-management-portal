"""Reports & Performance Summary — reads from ai_insights + grades/attendance."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.ai_insight import AIInsight, InsightType
from app.models.user import User, UserRole
from app.services import ai_engine
from app.services.academic_access import enrolled_students, list_accessible_classes


def student_report(db: Session, student: User) -> dict:
    """Full performance report for a single student."""
    snap = ai_engine.student_snapshot(db, student)
    texts = ai_engine.list_student_insight_texts(db, student, refresh=False)

    at_risk_row = (
        db.query(AIInsight)
        .filter(AIInsight.student_id == student.id, AIInsight.type == InsightType.at_risk)
        .order_by(AIInsight.created_at.desc())
        .first()
    )

    return {
        "student_id": student.id,
        "student_name": student.name,
        "attendance_percent": snap["attendance_percent"],
        "exam_average": snap["exam_average"],
        "assignments_submitted": snap["assignments_submitted"],
        "assignments_total": snap["assignments_total"],
        "grade_lines": snap["grade_lines"],
        "attendance_lines": snap["attendance_lines"],
        "at_risk": snap["at_risk"],
        "risk_reason": at_risk_row.content if at_risk_row else None,
        "weak_subjects": texts.get("weak_subjects", []),
        "ai_insights": texts.get("ai_insights", []),
        "ai_recommendations": texts.get("ai_recommendations", []),
    }


def class_report(db: Session, class_id: int) -> dict:
    """Class-level performance summary."""
    class_group = (
        db.query(ai_engine.ClassGroup)
        .filter(ai_engine.ClassGroup.id == class_id)
        .first()
    )
    if not class_group:
        return {"error": "Class not found"}

    students = enrolled_students(db, class_group)
    snapshots = [ai_engine.student_snapshot(db, s) for s in students]

    total_attendance = sum(s["attendance_percent"] for s in snapshots)
    total_exam = sum(s["exam_average"] for s in snapshots)
    at_risk_list = [s for s in snapshots if s["at_risk"]]

    class_insight = (
        db.query(AIInsight)
        .filter(AIInsight.class_id == class_id, AIInsight.type == InsightType.class_insight)
        .order_by(AIInsight.created_at.desc())
        .first()
    )

    return {
        "class_id": class_group.id,
        "class_name": class_group.name,
        "course_title": class_group.course.title if class_group.course else "",
        "student_count": len(students),
        "average_attendance": round(total_attendance / len(snapshots), 1) if snapshots else 0.0,
        "average_exam": round(total_exam / len(snapshots), 1) if snapshots else 0.0,
        "at_risk_count": len(at_risk_list),
        "at_risk_students": [
            {"id": s["student_id"], "name": s["name"], "attendance": s["attendance_percent"], "exam_avg": s["exam_average"]}
            for s in at_risk_list
        ],
        "class_insight": class_insight.content if class_insight else None,
        "student_summaries": [
            {
                "id": s["student_id"],
                "name": s["name"],
                "attendance": s["attendance_percent"],
                "exam_avg": s["exam_average"],
                "at_risk": s["at_risk"],
            }
            for s in snapshots
        ],
    }


def comparative_report(db: Session, actor: User) -> dict:
    """Compare performance across all accessible classes."""
    classes = list_accessible_classes(db, actor)
    class_summaries = []

    for cg in classes:
        students = enrolled_students(db, cg)
        snapshots = [ai_engine.student_snapshot(db, s) for s in students]
        if not snapshots:
            continue

        avg_att = round(sum(s["attendance_percent"] for s in snapshots) / len(snapshots), 1)
        avg_exam = round(sum(s["exam_average"] for s in snapshots) / len(snapshots), 1)
        at_risk_count = sum(1 for s in snapshots if s["at_risk"])

        class_summaries.append({
            "class_id": cg.id,
            "class_name": cg.name,
            "course_title": cg.course.title if cg.course else "",
            "student_count": len(students),
            "average_attendance": avg_att,
            "average_exam": avg_exam,
            "at_risk_count": at_risk_count,
        })

    total_students = sum(c["student_count"] for c in class_summaries)
    total_at_risk = sum(c["at_risk_count"] for c in class_summaries)

    rec_query = db.query(AIInsight).filter(AIInsight.type == InsightType.recommendation)
    if actor.role != UserRole.admin:
        student_ids = {student.id for cg in classes for student in enrolled_students(db, cg)}
        if not student_ids:
            rec_query = rec_query.filter(AIInsight.id == -1)
        else:
            rec_query = rec_query.filter(AIInsight.student_id.in_(student_ids))
    all_recommendations = rec_query.order_by(AIInsight.created_at.desc()).limit(20).all()

    return {
        "classes": class_summaries,
        "total_classes": len(class_summaries),
        "total_students": total_students,
        "total_at_risk": total_at_risk,
        "overall_at_risk_percent": round((total_at_risk / total_students) * 100, 1) if total_students else 0.0,
        "ai_recommendations_rollup": list({row.content for row in all_recommendations})[:10],
    }


def admin_insights_summary(db: Session) -> dict:
    """Rollup of all AI insights for admin dashboard."""
    performance_count = db.query(AIInsight).filter(AIInsight.type == InsightType.performance).count()
    at_risk_count = db.query(AIInsight).filter(AIInsight.type == InsightType.at_risk).count()
    weak_count = db.query(AIInsight).filter(AIInsight.type == InsightType.weak_subject).count()
    rec_count = db.query(AIInsight).filter(AIInsight.type == InsightType.recommendation).count()
    class_insight_count = db.query(AIInsight).filter(AIInsight.type == InsightType.class_insight).count()

    recent = (
        db.query(AIInsight)
        .order_by(AIInsight.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "insight_counts": {
            "performance": performance_count,
            "at_risk": at_risk_count,
            "weak_subject": weak_count,
            "recommendation": rec_count,
            "class_insight": class_insight_count,
        },
        "recent_insights": [
            {
                "type": row.type.value,
                "content": row.content[:200],
                "student_id": row.student_id,
                "class_id": row.class_id,
            }
            for row in recent
        ],
    }


def _pdf_text(value: object) -> str:
    text = str(value or "").replace("\r", " ")
    return text.encode("latin-1", "replace").decode("latin-1")


def student_report_pdf(db: Session, student: User) -> bytes:
    from fpdf import FPDF

    data = student_report(db, student)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()
    width = pdf.epw

    def heading(text: str) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(width, 8, _pdf_text(text))

    def body(text: str) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(width, 5, _pdf_text(text))

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(width, 10, "Performance Report")
    body(data["student_name"])
    pdf.ln(2)
    lines = [
        f"Attendance: {data['attendance_percent']}%",
        f"Exam average: {data['exam_average']}%",
        f"Assignments: {data['assignments_submitted']}/{data['assignments_total']}",
        f"At risk: {'Yes' if data['at_risk'] else 'No'}",
    ]
    if data.get("risk_reason"):
        lines.append(f"Risk note: {data['risk_reason']}")
    for line in lines:
        body(line)
    pdf.ln(2)
    heading("Grades")
    for line in data.get("grade_lines") or ["None recorded"]:
        body(f"- {line}")
    pdf.ln(2)
    heading("Weak subjects")
    for item in data.get("weak_subjects") or ["None flagged"]:
        body(f"- {item}")
    pdf.ln(2)
    heading("AI recommendations")
    for item in data.get("ai_recommendations") or ["None stored"]:
        body(f"- {item}")
    return bytes(pdf.output())
