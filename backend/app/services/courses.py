from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.assignment import Assignment
from app.models.attendance import Attendance
from app.models.course import Course
from app.models.exam import Exam
from app.models.user import User, UserRole
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate


def _to_out(course: Course, *, student_id: int | None = None) -> CourseOut:
    enrolled = False
    if student_id is not None:
        enrolled = any(e.student_id == student_id for e in course.enrollments)
    return CourseOut(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        teacher_id=course.teacher_id,
        teacher_name=course.teacher.name if course.teacher else "",
        schedule=course.schedule,
        rating=course.rating,
        syllabus=course.syllabus,
        class_count=len(course.classes),
        enrollment_count=len(course.enrollments),
        enrolled=enrolled,
    )


def _load_course(db: Session, course_id: int) -> Course:
    course = (
        db.query(Course)
        .options(
            joinedload(Course.teacher),
            joinedload(Course.classes),
            joinedload(Course.enrollments),
        )
        .filter(Course.id == course_id)
        .first()
    )
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


def list_courses(
    db: Session,
    *,
    search: str | None = None,
    category: str | None = None,
    teacher_id: int | None = None,
    sort: str | None = None,
    limit: int | None = None,
    student_id: int | None = None,
) -> list[CourseOut]:
    query = db.query(Course).options(
        joinedload(Course.teacher),
        joinedload(Course.classes),
        joinedload(Course.enrollments),
    )
    if teacher_id:
        query = query.filter(Course.teacher_id == teacher_id)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Course.title.ilike(term),
                Course.description.ilike(term),
                Course.category.ilike(term),
            )
        )
    if category:
        query = query.filter(Course.category == category)
    if sort == "rating":
        query = query.order_by(Course.rating.desc(), Course.title.asc())
    else:
        query = query.order_by(Course.title.asc())
    if limit:
        query = query.limit(limit)
    return [_to_out(course, student_id=student_id) for course in query.all()]


def list_categories(db: Session) -> list[str]:
    rows = db.query(Course.category).distinct().order_by(Course.category.asc()).all()
    return [row[0] for row in rows]


def get_course(db: Session, course_id: int, *, student_id: int | None = None) -> CourseOut:
    return _to_out(_load_course(db, course_id), student_id=student_id)


def _assert_teacher(db: Session, teacher_id: int) -> User:
    teacher = db.get(User, teacher_id)
    if teacher is None or teacher.role != UserRole.teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="teacher_id must belong to a teacher")
    return teacher


def create_course(db: Session, payload: CourseCreate, actor: User) -> CourseOut:
    if actor.role == UserRole.teacher:
        teacher_id = actor.id
        rating = 0.0
    else:
        if payload.teacher_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin must provide teacher_id when creating a course",
            )
        _assert_teacher(db, payload.teacher_id)
        teacher_id = payload.teacher_id
        rating = payload.rating if payload.rating is not None else 0.0

    course = Course(
        title=payload.title.strip(),
        description=payload.description.strip(),
        category=payload.category.strip(),
        teacher_id=teacher_id,
        schedule=payload.schedule.strip(),
        syllabus=payload.syllabus or "",
        rating=rating,
    )
    db.add(course)
    db.commit()
    return get_course(db, course.id)


def assert_can_manage_course(course: Course, actor: User) -> None:
    if actor.role == UserRole.admin:
        return
    if actor.role == UserRole.teacher and course.teacher_id == actor.id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You can only manage your own courses",
    )


def update_course(db: Session, course_id: int, payload: CourseUpdate, actor: User) -> CourseOut:
    course = _load_course(db, course_id)
    assert_can_manage_course(course, actor)

    data = payload.model_dump(exclude_unset=True)
    if actor.role != UserRole.admin:
        data.pop("teacher_id", None)
        data.pop("rating", None)
    elif "teacher_id" in data and data["teacher_id"] is not None:
        _assert_teacher(db, data["teacher_id"])

    for key, value in data.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(course, key, value)
    db.commit()
    return get_course(db, course.id)


def delete_course(db: Session, course_id: int, actor: User) -> None:
    course = _load_course(db, course_id)
    assert_can_manage_course(course, actor)

    class_ids = [c.id for c in course.classes]
    if class_ids:
        has_work = (
            db.query(func.count(Assignment.id)).filter(Assignment.class_id.in_(class_ids)).scalar()
            or db.query(func.count(Exam.id)).filter(Exam.class_id.in_(class_ids)).scalar()
            or db.query(func.count(Attendance.id)).filter(Attendance.class_id.in_(class_ids)).scalar()
        )
        if has_work:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete a course that still has attendance, assignments, or exams",
            )

    for enrollment in list(course.enrollments):
        db.delete(enrollment)
    for class_group in list(course.classes):
        db.delete(class_group)
    db.delete(course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete this course because related records still exist",
        )
