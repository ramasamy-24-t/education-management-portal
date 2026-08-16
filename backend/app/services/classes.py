from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.attendance import Attendance
from app.models.course import ClassGroup, Course
from app.models.exam import Exam
from app.models.user import User
from app.schemas.course import ClassCreate, ClassOut, ClassUpdate
from app.services.courses import assert_can_manage_course, _load_course


def list_classes(db: Session, course_id: int) -> list[ClassOut]:
    _load_course(db, course_id)
    rows = db.query(ClassGroup).filter(ClassGroup.course_id == course_id).order_by(ClassGroup.name.asc()).all()
    return [ClassOut.model_validate(row) for row in rows]


def create_class(db: Session, course_id: int, payload: ClassCreate, actor: User) -> ClassOut:
    course = _load_course(db, course_id)
    assert_can_manage_course(course, actor)
    class_group = ClassGroup(course_id=course.id, name=payload.name.strip())
    db.add(class_group)
    db.commit()
    db.refresh(class_group)
    return ClassOut.model_validate(class_group)


def _load_class(db: Session, class_id: int) -> ClassGroup:
    class_group = db.get(ClassGroup, class_id)
    if class_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    return class_group


def update_class(db: Session, class_id: int, payload: ClassUpdate, actor: User) -> ClassOut:
    class_group = _load_class(db, class_id)
    course = db.get(Course, class_group.course_id)
    assert_can_manage_course(course, actor)
    class_group.name = payload.name.strip()
    db.commit()
    db.refresh(class_group)
    return ClassOut.model_validate(class_group)


def delete_class(db: Session, class_id: int, actor: User) -> None:
    class_group = _load_class(db, class_id)
    course = db.get(Course, class_group.course_id)
    assert_can_manage_course(course, actor)

    has_work = (
        db.query(func.count(Assignment.id)).filter(Assignment.class_id == class_id).scalar()
        or db.query(func.count(Exam.id)).filter(Exam.class_id == class_id).scalar()
        or db.query(func.count(Attendance.id)).filter(Attendance.class_id == class_id).scalar()
    )
    if has_work:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a class that still has attendance, assignments, or exams",
        )
    db.delete(class_group)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete this class because related records still exist",
        )
