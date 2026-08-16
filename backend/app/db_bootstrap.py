from datetime import date, datetime, timedelta, timezone
import json

from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload

from app.constants import (
    DEFAULT_EXAM_QUESTIONS,
    DEFAULT_SCHOOL_NAME,
    DEFAULT_SCHOOL_SLUG,
    DEMO_EMAIL_DOMAIN,
    FALLBACK_STUDY_TIPS,
    SECOND_SCHOOL_NAME,
    SECOND_SCHOOL_SLUG,
    questions_for_course,
)
from app.database import Base, SessionLocal, engine
from app.models import (  # noqa: F401 — register metadata
    AIInsight,
    Announcement,
    Assignment,
    AssignmentSubmission,
    AssistantMessage,
    AssistantRateHit,
    Attendance,
    AttendanceStatus,
    ClassGroup,
    ContactMessage,
    Course,
    Enrollment,
    Exam,
    ExamAnalysis,
    ExamAttempt,
    FAQ,
    Grade,
    PracticeQuestionSet,
    School,
    StudyTip,
    User,
    UserRole,
)


def _add_column_if_missing(conn, table: str, column: str, ddl: str) -> None:
    try:
        exists = conn.execute(text(f"SHOW COLUMNS FROM `{table}` LIKE '{column}'")).fetchone()
    except Exception:
        conn.rollback()
        return
    if exists is None:
        conn.execute(text(f"ALTER TABLE `{table}` ADD COLUMN {ddl}"))
        conn.commit()


def _drop_column_if_exists(conn, table: str, column: str) -> None:
    try:
        exists = conn.execute(text(f"SHOW COLUMNS FROM `{table}` LIKE '{column}'")).fetchone()
    except Exception:
        conn.rollback()
        return
    if exists is not None:
        conn.execute(text(f"ALTER TABLE `{table}` DROP COLUMN `{column}`"))
        conn.commit()


def _table_exists(conn, table: str) -> bool:
    row = conn.execute(text(f"SHOW TABLES LIKE '{table}'")).fetchone()
    return row is not None


def ensure_schema() -> None:
    """Create new tables and add columns without wiping existing data."""
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        _add_column_if_missing(conn, "users", "is_active", "is_active TINYINT(1) NOT NULL DEFAULT 1")
        _drop_column_if_exists(conn, "users", "is_verified")
        _drop_column_if_exists(conn, "users", "verify_token")
        _add_column_if_missing(conn, "users", "school_id", "school_id INT NULL")
        _add_column_if_missing(conn, "courses", "school_id", "school_id INT NULL")
        _add_column_if_missing(conn, "ai_insights", "trend", "trend VARCHAR(32) NULL")
        _add_column_if_missing(conn, "ai_insights", "trend_reason", "trend_reason TEXT NULL")
        _add_column_if_missing(conn, "assignment_submissions", "file_path", "file_path VARCHAR(500) NULL")
        _add_column_if_missing(
            conn, "assignment_submissions", "original_filename", "original_filename VARCHAR(255) NULL"
        )
        _add_column_if_missing(conn, "exams", "questions_json", "questions_json TEXT NULL")
        if _table_exists(conn, "users"):
            conn.execute(
                text(
                    "UPDATE users SET email = REPLACE(email, '@edu.local', :domain) "
                    "WHERE email LIKE '%@edu.local'"
                ),
                {"domain": f"@{DEMO_EMAIL_DOMAIN}"},
            )
            conn.commit()
        if _table_exists(conn, "exams"):
            conn.execute(text("UPDATE exams SET questions_json = '[]' WHERE questions_json IS NULL"))
            conn.commit()

    db = SessionLocal()
    try:
        _ensure_schools(db)
        _assign_school_ids(db)
        _backfill_attendance(db)
        _ensure_exam_questions(db)
        _ensure_prior_window_exams(db)
        _ensure_live_quizzes(db)
        _ensure_study_tips(db)
        db.commit()
    finally:
        db.close()


def _ensure_schools(db: Session) -> None:
    if db.query(School).filter(School.slug == DEFAULT_SCHOOL_SLUG).first() is None:
        db.add(School(name=DEFAULT_SCHOOL_NAME, slug=DEFAULT_SCHOOL_SLUG))
    if db.query(School).filter(School.slug == SECOND_SCHOOL_SLUG).first() is None:
        db.add(School(name=SECOND_SCHOOL_NAME, slug=SECOND_SCHOOL_SLUG))
    db.flush()


def _default_school(db: Session) -> School:
    school = db.query(School).filter(School.slug == DEFAULT_SCHOOL_SLUG).first()
    if school is None:
        school = School(name=DEFAULT_SCHOOL_NAME, slug=DEFAULT_SCHOOL_SLUG)
        db.add(school)
        db.flush()
    return school


def _assign_school_ids(db: Session) -> None:
    school = _default_school(db)
    db.query(User).filter(User.school_id.is_(None)).update({User.school_id: school.id}, synchronize_session=False)
    db.query(Course).filter(Course.school_id.is_(None)).update({Course.school_id: school.id}, synchronize_session=False)


def _backfill_attendance(db: Session) -> None:
    """Fill ~28 days so 14-day vs prior-14-day risk trend has data."""
    today = date.today()
    enrollments = db.query(Enrollment).all()
    classes_by_course: dict[int, list[ClassGroup]] = {}
    for class_group in db.query(ClassGroup).all():
        classes_by_course.setdefault(class_group.course_id, []).append(class_group)

    existing = {
        (row.student_id, row.class_id, row.date)
        for row in db.query(Attendance.student_id, Attendance.class_id, Attendance.date).all()
    }
    to_add: list[Attendance] = []
    for enrollment in enrollments:
        for class_group in classes_by_course.get(enrollment.course_id, []):
            for offset in range(1, 29):
                day = today - timedelta(days=offset)
                key = (enrollment.student_id, class_group.id, day)
                if key in existing:
                    continue
                status = AttendanceStatus.present
                if offset % 11 == 0 and enrollment.student_id % 2 == 0:
                    status = AttendanceStatus.absent
                elif offset % 8 == 0:
                    status = AttendanceStatus.late
                to_add.append(
                    Attendance(
                        student_id=enrollment.student_id,
                        class_id=class_group.id,
                        date=day,
                        status=status,
                    )
                )
                existing.add(key)
    if to_add:
        db.add_all(to_add)


def _ensure_exam_questions(db: Session) -> None:
    generic = json.dumps(DEFAULT_EXAM_QUESTIONS)
    exams = (
        db.query(Exam)
        .options(joinedload(Exam.class_group).joinedload(ClassGroup.course))
        .all()
    )
    for exam in exams:
        raw = (exam.questions_json or "").strip()
        course = exam.class_group.course if exam.class_group else None
        payload = json.dumps(
            questions_for_course(
                course.title if course else "",
                course.category if course else "",
            )
        )
        if not raw or raw == "[]" or raw == generic:
            exam.questions_json = payload


def _ensure_study_tips(db: Session) -> None:
    if db.query(StudyTip).count() >= 3:
        return
    now = datetime.now(timezone.utc)
    for tip in FALLBACK_STUDY_TIPS:
        db.add(StudyTip(content=tip, source="fallback", created_at=now))


def _ensure_prior_window_exams(db: Session) -> None:
    """Add a checkpoint exam ~20 days ago so the prior 14-day window can include grades."""
    today = date.today()
    prior_date = today - timedelta(days=20)
    cutoff = today - timedelta(days=14)
    classes = db.query(ClassGroup).all()
    enrollments = db.query(Enrollment).all()
    students_by_course: dict[int, list[int]] = {}
    for row in enrollments:
        students_by_course.setdefault(row.course_id, []).append(row.student_id)

    for class_group in classes:
        has_prior = (
            db.query(Exam)
            .filter(Exam.class_id == class_group.id, Exam.date < cutoff)
            .first()
        )
        if has_prior:
            continue
        course_title = class_group.course.title if class_group.course else "Course"
        exam = Exam(
            class_id=class_group.id,
            title=f"{course_title} Checkpoint",
            date=prior_date,
            max_marks=100,
            questions_json=json.dumps(
                questions_for_course(
                    course_title,
                    class_group.course.category if class_group.course else "",
                )
            ),
        )
        db.add(exam)
        db.flush()
        for i, student_id in enumerate(students_by_course.get(class_group.course_id, [])):
            marks = 58 + i * 7
            db.add(Grade(exam_id=exam.id, student_id=student_id, marks_obtained=marks))


def _ensure_live_quizzes(db: Session) -> None:
    today = date.today()
    for class_group in db.query(ClassGroup).all():
        exists = (
            db.query(Exam)
            .filter(Exam.class_id == class_group.id, Exam.title.like("%Practice Quiz%"))
            .first()
        )
        if exists:
            continue
        course_title = class_group.course.title if class_group.course else "Course"
        db.add(
            Exam(
                class_id=class_group.id,
                title=f"{course_title} Practice Quiz",
                date=today,
                max_marks=100,
                questions_json=json.dumps(
                    questions_for_course(
                        course_title,
                        class_group.course.category if class_group.course else "",
                    )
                ),
            )
        )

