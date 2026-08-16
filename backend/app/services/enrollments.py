from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.user import User, UserRole
from app.schemas.enrollment import EnrollmentOut
from app.services.courses import _load_course


def enroll_student(db: Session, course_id: int, student: User) -> EnrollmentOut:
    if student.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in a course",
        )
    course = _load_course(db, course_id)
    if student.school_id and course.school_id and student.school_id != course.school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only enroll in courses at your school",
        )
    existing = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.id, Enrollment.course_id == course.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already enrolled in this course")

    enrollment = Enrollment(student_id=student.id, course_id=course.id)
    db.add(enrollment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already enrolled in this course")
    db.refresh(enrollment)
    return EnrollmentOut(
        id=enrollment.id,
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=enrollment.enrolled_at,
        course_title=course.title,
    )


def list_my_enrollments(db: Session, student: User) -> list[EnrollmentOut]:
    rows = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )
    return [
        EnrollmentOut(
            id=row.id,
            student_id=row.student_id,
            course_id=row.course_id,
            enrolled_at=row.enrolled_at,
            course_title=row.course.title if row.course else None,
        )
        for row in rows
    ]
