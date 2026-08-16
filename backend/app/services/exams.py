from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.course import ClassGroup
from app.models.exam import Exam, Grade
from app.models.user import User, UserRole
from app.schemas.academic import ExamCreate, ExamGradesRequest, ExamOut, GradeOut
from app.services.academic_access import (
    assert_can_manage_class,
    can_view_class,
    enrolled_students,
    list_accessible_classes,
    load_class,
)


def _exam_out(exam: Exam) -> ExamOut:
    class_group = exam.class_group
    course = class_group.course if class_group else None
    return ExamOut(
        id=exam.id,
        class_id=exam.class_id,
        class_name=class_group.name if class_group else "",
        course_title=course.title if course else "",
        title=exam.title,
        date=exam.date,
        max_marks=exam.max_marks,
    )


def _grade_out(row: Grade) -> GradeOut:
    exam = row.exam
    class_group = exam.class_group if exam else None
    course = class_group.course if class_group else None
    max_marks = exam.max_marks if exam else 0
    percent = round((row.marks_obtained / max_marks) * 100, 1) if max_marks else 0.0
    return GradeOut(
        id=row.id,
        exam_id=row.exam_id,
        exam_title=exam.title if exam else "",
        student_id=row.student_id,
        student_name=row.student.name if row.student else "",
        class_name=class_group.name if class_group else "",
        course_title=course.title if course else "",
        date=exam.date if exam else None,
        max_marks=max_marks,
        marks_obtained=row.marks_obtained,
        percent=percent,
    )


def create_exam(db: Session, payload: ExamCreate, actor: User) -> ExamOut:
    class_group = load_class(db, payload.class_id)
    assert_can_manage_class(class_group, actor)
    exam = Exam(
        class_id=class_group.id,
        title=payload.title.strip(),
        date=payload.date,
        max_marks=payload.max_marks,
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return _exam_out(exam)


def list_exams(db: Session, actor: User, *, class_id: int | None = None) -> list[ExamOut]:
    query = db.query(Exam).options(joinedload(Exam.class_group).joinedload(ClassGroup.course))
    if class_id:
        class_group = load_class(db, class_id)
        if not can_view_class(db, class_group, actor):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this class")
        query = query.filter(Exam.class_id == class_id)
    else:
        class_ids = [item.id for item in list_accessible_classes(db, actor)]
        if not class_ids:
            return []
        query = query.filter(Exam.class_id.in_(class_ids))
    return [_exam_out(row) for row in query.order_by(Exam.date.desc()).all()]


def get_exam(db: Session, exam_id: int, actor: User) -> Exam:
    exam = (
        db.query(Exam)
        .options(joinedload(Exam.class_group).joinedload(ClassGroup.course))
        .filter(Exam.id == exam_id)
        .first()
    )
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    class_group = load_class(db, exam.class_id)
    if not can_view_class(db, class_group, actor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this exam")
    return exam


def record_grades(db: Session, exam_id: int, payload: ExamGradesRequest, actor: User) -> list[GradeOut]:
    exam = get_exam(db, exam_id, actor)
    class_group = load_class(db, exam.class_id)
    assert_can_manage_class(class_group, actor)
    roster_ids = {student.id for student in enrolled_students(db, class_group)}

    results: list[Grade] = []
    for record in payload.records:
        if record.student_id not in roster_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student {record.student_id} is not enrolled in this course",
            )
        if record.marks_obtained > exam.max_marks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Marks cannot exceed max_marks ({exam.max_marks})",
            )
        existing = (
            db.query(Grade)
            .filter(Grade.exam_id == exam.id, Grade.student_id == record.student_id)
            .first()
        )
        if existing:
            existing.marks_obtained = record.marks_obtained
            results.append(existing)
        else:
            row = Grade(exam_id=exam.id, student_id=record.student_id, marks_obtained=record.marks_obtained)
            db.add(row)
            results.append(row)
    db.commit()
    ids = [row.id for row in results]
    rows = (
        db.query(Grade)
        .options(
            joinedload(Grade.student),
            joinedload(Grade.exam).joinedload(Exam.class_group).joinedload(ClassGroup.course),
        )
        .filter(Grade.id.in_(ids))
        .all()
    )
    return [_grade_out(row) for row in rows]


def list_exam_grades(db: Session, exam_id: int, actor: User) -> list[GradeOut]:
    exam = get_exam(db, exam_id, actor)
    query = (
        db.query(Grade)
        .options(
            joinedload(Grade.student),
            joinedload(Grade.exam).joinedload(Exam.class_group).joinedload(ClassGroup.course),
        )
        .filter(Grade.exam_id == exam.id)
    )
    if actor.role == UserRole.student:
        query = query.filter(Grade.student_id == actor.id)
    else:
        assert_can_manage_class(load_class(db, exam.class_id), actor)
    return [_grade_out(row) for row in query.order_by(Grade.student_id.asc()).all()]


def my_grade_history(db: Session, student: User) -> list[GradeOut]:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students have a grade history")
    rows = (
        db.query(Grade)
        .options(
            joinedload(Grade.exam).joinedload(Exam.class_group).joinedload(ClassGroup.course),
            joinedload(Grade.student),
        )
        .filter(Grade.student_id == student.id)
        .all()
    )
    return sorted([_grade_out(row) for row in rows], key=lambda item: item.date, reverse=True)
