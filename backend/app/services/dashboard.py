from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.academic import ClassContextOut
from app.schemas.dashboard import (
    AssignmentWithSubmission,
    ProgressOverviewOut,
    StudentDashboardOut,
    TeacherDashboardOut,
)
from app.schemas.user import UserPublic
from app.services.academic_access import list_accessible_classes
from app.services.assignments import list_assignments, my_submissions
from app.services.attendance import attendance_summary
from app.services.courses import list_courses
from app.services.exams import my_grade_history


def _class_out(row) -> ClassContextOut:
    return ClassContextOut(
        id=row.id,
        name=row.name,
        course_id=row.course_id,
        course_title=row.course.title if row.course else "",
        teacher_id=row.course.teacher_id if row.course else 0,
    )


def student_progress(db: Session, student: User) -> ProgressOverviewOut:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Progress overview is student-only")

    classes = list_accessible_classes(db, student)
    summaries = []
    for class_group in classes:
        summaries.extend(attendance_summary(db, student, class_id=class_group.id))
    attendance_percent = (
        round(sum(item.percent_present for item in summaries) / len(summaries), 1) if summaries else 0.0
    )

    grades = my_grade_history(db, student)
    average_exam = round(sum(item.percent for item in grades) / len(grades), 1) if grades else 0.0

    assignments = list_assignments(db, student)
    submissions = my_submissions(db, student)
    submitted_ids = {row.assignment_id for row in submissions}
    graded = [row.grade for row in submissions if row.grade is not None]
    completion = round((len(submitted_ids) / len(assignments)) * 100, 1) if assignments else 0.0

    return ProgressOverviewOut(
        attendance_percent=attendance_percent,
        average_exam_percent=average_exam,
        assignments_submitted=len(submitted_ids),
        assignments_total=len(assignments),
        assignment_completion_percent=completion,
        average_assignment_grade=round(sum(graded) / len(graded), 1) if graded else None,
        course_count=len({item.course_id for item in classes}),
        weak_subjects=[],
        improvement_tips=[],
        ai_insights=[],
        ai_pending=True,
    )


def student_dashboard(db: Session, student: User) -> StudentDashboardOut:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student dashboard only")
    assignments = list_assignments(db, student)
    submissions = {row.assignment_id: row for row in my_submissions(db, student)}
    classes = list_accessible_classes(db, student)
    attendance = []
    for class_group in classes:
        attendance.extend(attendance_summary(db, student, class_id=class_group.id))
    return StudentDashboardOut(
        profile=UserPublic.model_validate(student),
        courses=[course for course in list_courses(db, student_id=student.id) if course.enrolled],
        assignments=[
            AssignmentWithSubmission(**item.model_dump(), my_submission=submissions.get(item.id))
            for item in assignments
        ],
        attendance=attendance,
        grades=my_grade_history(db, student),
        progress_overview=student_progress(db, student),
        ai_recommendations=[],
    )


def teacher_dashboard(db: Session, teacher: User) -> TeacherDashboardOut:
    if teacher.role != UserRole.teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher dashboard only")
    return TeacherDashboardOut(
        profile=UserPublic.model_validate(teacher),
        courses=list_courses(db, teacher_id=teacher.id),
        classes=[_class_out(row) for row in list_accessible_classes(db, teacher)],
    )
