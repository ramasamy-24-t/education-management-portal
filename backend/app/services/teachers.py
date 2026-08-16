from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole
from app.schemas.user import TeacherPublic, UserPublic


def list_teachers(db: Session) -> list[UserPublic]:
    rows = (
        db.query(User)
        .filter(User.role == UserRole.teacher)
        .order_by(User.name.asc())
        .all()
    )
    return [UserPublic.model_validate(row) for row in rows]


def top_teachers(db: Session, *, limit: int = 5) -> list[TeacherPublic]:
    student_count = func.count(func.distinct(Enrollment.student_id))
    avg_rating = func.coalesce(func.avg(Course.rating), 0.0)
    course_count = func.count(func.distinct(Course.id))

    rows = (
        db.query(User, avg_rating.label("average_rating"), course_count.label("course_count"), student_count.label("student_count"))
        .join(Course, Course.teacher_id == User.id)
        .outerjoin(Enrollment, Enrollment.course_id == Course.id)
        .filter(User.role == UserRole.teacher)
        .group_by(User.id)
        .order_by(avg_rating.desc(), student_count.desc(), User.name.asc())
        .limit(limit)
        .all()
    )
    results: list[TeacherPublic] = []
    for user, average_rating, course_count_val, student_count_val in rows:
        base = UserPublic.model_validate(user)
        results.append(
            TeacherPublic(
                **base.model_dump(),
                average_rating=round(float(average_rating or 0), 2),
                course_count=int(course_count_val or 0),
                student_count=int(student_count_val or 0),
            )
        )
    return results
