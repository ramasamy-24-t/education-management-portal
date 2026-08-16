"""Create the MySQL database (if needed), tables, and sample data."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Load backend/.env regardless of the working directory.
load_dotenv(Path(__file__).resolve().parent / ".env")

from app.config import get_settings  # noqa: E402
from app.database import Base  # noqa: E402
from app.models import (  # noqa: E402
    AIInsight,
    Announcement,
    Assignment,
    AssignmentSubmission,
    Attendance,
    AttendanceStatus,
    ClassGroup,
    ContactMessage,
    Course,
    Enrollment,
    Exam,
    ExamAnalysis,
    FAQ,
    Grade,
    InsightType,
    User,
    UserRole,
)
from app.services.security import hash_password  # noqa: E402

DEFAULT_PASSWORD = "password123"


def ensure_database() -> None:
    settings = get_settings()
    engine = create_engine(settings.server_database_url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{settings.db_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        conn.commit()
    engine.dispose()


def seed(session: Session) -> None:
    if session.query(User).first():
        print("Database already has users — skipping seed.")
        return

    hash_pw = hash_password(DEFAULT_PASSWORD)

    admin = User(
        name="Asha Menon",
        email="admin@edu.local",
        password_hash=hash_pw,
        role=UserRole.admin,
    )
    teachers = [
        User(name="Dr. Priya Nair", email="priya.nair@edu.local", password_hash=hash_pw, role=UserRole.teacher),
        User(name="Prof. Arjun Mehta", email="arjun.mehta@edu.local", password_hash=hash_pw, role=UserRole.teacher),
        User(name="Ms. Kavya Reddy", email="kavya.reddy@edu.local", password_hash=hash_pw, role=UserRole.teacher),
    ]
    students = [
        User(name="Rohan Sharma", email="rohan.sharma@edu.local", password_hash=hash_pw, role=UserRole.student),
        User(name="Ananya Iyer", email="ananya.iyer@edu.local", password_hash=hash_pw, role=UserRole.student),
        User(name="Vikram Patel", email="vikram.patel@edu.local", password_hash=hash_pw, role=UserRole.student),
        User(name="Meera Joshi", email="meera.joshi@edu.local", password_hash=hash_pw, role=UserRole.student),
        User(name="Sahil Khan", email="sahil.khan@edu.local", password_hash=hash_pw, role=UserRole.student),
    ]
    session.add_all([admin, *teachers, *students])
    session.flush()

    courses_data = [
        {
            "title": "Introduction to Python",
            "description": "Write programs, work with data, and build small apps in Python.",
            "category": "Computer Science",
            "teacher": teachers[0],
            "schedule": "Mon / Wed 10:00–11:30",
            "rating": 4.8,
            "syllabus": "1. Syntax\n2. Data structures\n3. Functions\n4. Files\n5. Mini project",
            "class_name": "CS101-A",
        },
        {
            "title": "Linear Algebra",
            "description": "Vectors, matrices, and linear transformations for STEM majors.",
            "category": "Mathematics",
            "teacher": teachers[1],
            "schedule": "Tue / Thu 09:00–10:30",
            "rating": 4.6,
            "syllabus": "1. Vectors\n2. Matrices\n3. Determinants\n4. Eigenvalues\n5. Applications",
            "class_name": "MATH201-B",
        },
        {
            "title": "World History: 1900–Present",
            "description": "Political, social, and economic change across the twentieth century.",
            "category": "Humanities",
            "teacher": teachers[2],
            "schedule": "Fri 13:00–16:00",
            "rating": 4.4,
            "syllabus": "1. World wars\n2. Cold War\n3. Decolonization\n4. Globalization",
            "class_name": "HIST110-A",
        },
        {
            "title": "Data Structures",
            "description": "Arrays, trees, graphs, and complexity analysis.",
            "category": "Computer Science",
            "teacher": teachers[0],
            "schedule": "Mon / Wed 14:00–15:30",
            "rating": 4.7,
            "syllabus": "1. Arrays & lists\n2. Stacks & queues\n3. Trees\n4. Graphs\n5. Hashing",
            "class_name": "CS201-A",
        },
        {
            "title": "Statistics for Decision Making",
            "description": "Descriptive stats, probability, and inference for real datasets.",
            "category": "Mathematics",
            "teacher": teachers[1],
            "schedule": "Tue / Thu 11:00–12:30",
            "rating": 4.3,
            "syllabus": "1. Descriptive stats\n2. Probability\n3. Sampling\n4. Hypothesis tests",
            "class_name": "STAT101-A",
        },
    ]

    courses: list[Course] = []
    classes: list[ClassGroup] = []
    for item in courses_data:
        course = Course(
            title=item["title"],
            description=item["description"],
            category=item["category"],
            teacher_id=item["teacher"].id,
            schedule=item["schedule"],
            rating=item["rating"],
            syllabus=item["syllabus"],
        )
        session.add(course)
        session.flush()
        class_group = ClassGroup(course_id=course.id, name=item["class_name"])
        session.add(class_group)
        courses.append(course)
        classes.append(class_group)
    session.flush()

    # Each student enrolls in 3 courses.
    enroll_map = [
        (students[0], [0, 1, 3]),
        (students[1], [0, 2, 4]),
        (students[2], [1, 3, 4]),
        (students[3], [0, 1, 2]),
        (students[4], [2, 3, 4]),
    ]
    for student, course_idxs in enroll_map:
        for idx in course_idxs:
            session.add(Enrollment(student_id=student.id, course_id=courses[idx].id))
    session.flush()

    today = date.today()
    for class_group, course in zip(classes, courses):
        enrolled_students = [
            student
            for student, idxs in enroll_map
            if courses.index(course) in idxs
        ]
        for day_offset in range(5):
            day = today - timedelta(days=day_offset + 1)
            for i, student in enumerate(enrolled_students):
                status = AttendanceStatus.present
                if i == 0 and day_offset == 0:
                    status = AttendanceStatus.absent
                elif i == 1 and day_offset == 2:
                    status = AttendanceStatus.late
                session.add(
                    Attendance(
                        student_id=student.id,
                        class_id=class_group.id,
                        date=day,
                        status=status,
                    )
                )

    due = datetime.now(timezone.utc) + timedelta(days=7)
    past_due = datetime.now(timezone.utc) - timedelta(days=3)
    assignments: list[Assignment] = []
    for class_group, course in zip(classes, courses):
        a1 = Assignment(
            class_id=class_group.id,
            title=f"{course.title} — Problem Set 1",
            description="Complete the listed exercises and upload your write-up.",
            due_date=due,
        )
        a2 = Assignment(
            class_id=class_group.id,
            title=f"{course.title} — Reflection",
            description="Short reflection on this week's lectures.",
            due_date=past_due,
        )
        session.add_all([a1, a2])
        assignments.extend([a1, a2])
    session.flush()

    for assignment in assignments:
        course = next(c for c, cl in zip(courses, classes) if cl.id == assignment.class_id)
        enrolled_students = [
            student
            for student, idxs in enroll_map
            if courses.index(course) in idxs
        ]
        for i, student in enumerate(enrolled_students):
            if assignment.due_date < datetime.now(timezone.utc) and i == len(enrolled_students) - 1:
                continue  # one missing submission for variety
            session.add(
                AssignmentSubmission(
                    assignment_id=assignment.id,
                    student_id=student.id,
                    content=f"Submission from {student.name} for {assignment.title}.",
                    grade=78.0 + (i * 4) if assignment.due_date < datetime.now(timezone.utc) else None,
                    feedback="Solid effort; review the last section."
                    if assignment.due_date < datetime.now(timezone.utc)
                    else None,
                    ai_feedback="Clear structure. Strengthen examples in the conclusion."
                    if assignment.due_date < datetime.now(timezone.utc)
                    else None,
                )
            )

    exams: list[Exam] = []
    for class_group, course in zip(classes, courses):
        exam = Exam(
            class_id=class_group.id,
            title=f"{course.title} Midterm",
            date=today - timedelta(days=10),
            max_marks=100,
        )
        session.add(exam)
        exams.append(exam)
    session.flush()

    for exam, course in zip(exams, courses):
        enrolled_students = [
            student
            for student, idxs in enroll_map
            if courses.index(course) in idxs
        ]
        for i, student in enumerate(enrolled_students):
            marks = 62 + i * 8
            session.add(Grade(exam_id=exam.id, student_id=student.id, marks_obtained=marks))
            session.add(
                ExamAnalysis(
                    student_id=student.id,
                    exam_id=exam.id,
                    ai_summary=f"{student.name} scored {marks}/100 on {exam.title}.",
                    weak_topics="Proof writing; applied word problems"
                    if marks < 75
                    else "Minor gaps in advanced applications",
                )
            )

    session.add_all(
        [
            FAQ(
                question="How do I enroll in a course?",
                answer="Open Course Details and use Enroll Now. You must be logged in as a student.",
            ),
            FAQ(
                question="Who can mark attendance?",
                answer="Teachers mark attendance for classes they own. Students can view their own records.",
            ),
            FAQ(
                question="Where do AI recommendations come from?",
                answer="The AI Engine uses attendance, assignments, exams, and grades to generate insights.",
            ),
            FAQ(
                question="How do I contact support?",
                answer="Use the Contact form on the Contact page. An admin will follow up by email.",
            ),
        ]
    )

    session.add_all(
        [
            Announcement(
                title="Semester kickoff",
                body="Welcome back. Check your dashboard for new assignments and the midterm schedule.",
            ),
            Announcement(
                title="AI study tips are live",
                body="Open My Progress to see weak-subject tips generated from your latest exam analysis.",
            ),
        ]
    )

    session.add(
        ContactMessage(
            name="Parent Visitor",
            email="parent@example.com",
            message="Could you share office hours for Linear Algebra?",
        )
    )

    # AI Engine sample outputs (student-level and class-level).
    session.add(
        AIInsight(
            student_id=students[0].id,
            class_id=classes[1].id,
            type=InsightType.at_risk,
            content="Rohan missed a recent Linear Algebra session and scored below 75 on the midterm.",
        )
    )
    session.add(
        AIInsight(
            student_id=students[0].id,
            class_id=classes[0].id,
            type=InsightType.weak_subject,
            content="Proof-style questions in Linear Algebra are a weak area; Python fundamentals are strong.",
        )
    )
    session.add(
        AIInsight(
            student_id=students[0].id,
            class_id=None,
            type=InsightType.recommendation,
            content="Review eigenvectors before the next problem set. Use the AI study tips on Home.",
        )
    )
    session.add(
        AIInsight(
            student_id=students[1].id,
            class_id=classes[0].id,
            type=InsightType.performance,
            content="Ananya is consistent in Python with high attendance and assignment scores.",
        )
    )
    session.add(
        AIInsight(
            student_id=None,
            class_id=classes[0].id,
            type=InsightType.class_insight,
            content="CS101-A average midterm is solid; two students need follow-up on file I/O.",
        )
    )

    session.commit()
    print("Seed complete.")
    print("All accounts use password: password123")
    print("Admin:   admin@edu.local")
    print("Teacher: priya.nair@edu.local")
    print("Student: rohan.sharma@edu.local")


def main() -> None:
    ensure_database()
    settings = get_settings()
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        seed(session)
    engine.dispose()


if __name__ == "__main__":
    main()
