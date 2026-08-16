from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.course import ClassGroup, Course
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole


def load_class(db: Session, class_id: int) -> ClassGroup:
    class_group = (
        db.query(ClassGroup)
        .options(joinedload(ClassGroup.course))
        .filter(ClassGroup.id == class_id)
        .first()
    )
    if class_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    return class_group


def assert_can_manage_class(class_group: ClassGroup, actor: User) -> None:
    course = class_group.course
    if actor.role == UserRole.admin:
        return
    if actor.role == UserRole.teacher and course.teacher_id == actor.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You can only manage classes for your own courses",
    )


def assert_enrolled_in_class(db: Session, class_group: ClassGroup, student: User) -> None:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can do this")
    enrolled = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.id, Enrollment.course_id == class_group.course_id)
        .first()
    )
    if enrolled is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in this course",
        )


def enrolled_students(db: Session, class_group: ClassGroup) -> list[User]:
    return (
        db.query(User)
        .join(Enrollment, Enrollment.student_id == User.id)
        .filter(Enrollment.course_id == class_group.course_id, User.role == UserRole.student)
        .order_by(User.name.asc())
        .all()
    )


def list_accessible_classes(db: Session, actor: User) -> list[ClassGroup]:
    query = db.query(ClassGroup).options(joinedload(ClassGroup.course)).join(Course)
    if actor.role == UserRole.teacher:
        query = query.filter(Course.teacher_id == actor.id)
    elif actor.role == UserRole.student:
        query = query.join(Enrollment, Enrollment.course_id == Course.id).filter(Enrollment.student_id == actor.id)
    elif actor.role != UserRole.admin:
        return []
    return query.order_by(Course.title.asc(), ClassGroup.name.asc()).all()


def can_view_class(db: Session, class_group: ClassGroup, actor: User) -> bool:
    if actor.role == UserRole.admin:
        return True
    if actor.role == UserRole.teacher:
        return class_group.course.teacher_id == actor.id
    if actor.role == UserRole.student:
        return (
            db.query(Enrollment)
            .filter(Enrollment.student_id == actor.id, Enrollment.course_id == class_group.course_id)
            .first()
            is not None
        )
    return False
