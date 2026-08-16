"""Exam papers, attempts, and teacher-recorded grades."""

from __future__ import annotations

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.constants import questions_for_course
from app.models.course import ClassGroup
from app.models.exam import Exam, ExamAnalysis, ExamAttempt, Grade
from app.models.user import User, UserRole
from app.schemas.academic import (
    ExamAttemptOut,
    ExamAttemptRequest,
    ExamCreate,
    ExamGradesRequest,
    ExamOut,
    ExamPaperOut,
    ExamQuestionPublic,
    GradeOut,
)
from app.services.academic_access import (
    assert_can_manage_class,
    can_view_class,
    enrolled_students,
    list_accessible_classes,
    load_class,
)


def _questions(exam: Exam) -> list[dict]:
    try:
        data = json.loads(exam.questions_json or "[]")
    except json.JSONDecodeError:
        data = []
    return data if isinstance(data, list) else []


def exam_out(
    exam: Exam,
    *,
    attempted: bool = False,
    has_grade: bool = False,
) -> ExamOut:
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
        question_count=len(_questions(exam)),
        attempted=attempted,
        has_grade=has_grade,
    )


def _analysis_map(db: Session, exam_id: int | None = None, student_id: int | None = None) -> dict[tuple[int, int], ExamAnalysis]:
    query = db.query(ExamAnalysis)
    if exam_id:
        query = query.filter(ExamAnalysis.exam_id == exam_id)
    if student_id:
        query = query.filter(ExamAnalysis.student_id == student_id)
    return {(row.exam_id, row.student_id): row for row in query.all()}


def _grade_out(row: Grade, analysis: ExamAnalysis | None = None) -> GradeOut:
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
        ai_summary=analysis.ai_summary if analysis else None,
        weak_topics=analysis.weak_topics if analysis else None,
    )


def create_exam(db: Session, payload: ExamCreate, actor: User) -> ExamOut:
    class_group = load_class(db, payload.class_id)
    assert_can_manage_class(class_group, actor)
    if payload.questions:
        questions = [item.model_dump() for item in payload.questions]
    else:
        course = class_group.course
        questions = questions_for_course(
            course.title if course else "",
            course.category if course else "",
        )
    exam = Exam(
        class_id=class_group.id,
        title=payload.title.strip(),
        date=payload.date,
        max_marks=payload.max_marks,
        questions_json=json.dumps(questions),
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam_out(exam)


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
    rows = query.order_by(Exam.date.desc()).all()
    attempted_ids: set[int] = set()
    graded_ids: set[int] = set()
    if actor.role == UserRole.student and rows:
        exam_ids = [row.id for row in rows]
        attempted_ids = {
            exam_id
            for (exam_id,) in db.query(ExamAttempt.exam_id).filter(
                ExamAttempt.student_id == actor.id, ExamAttempt.exam_id.in_(exam_ids)
            )
        }
        graded_ids = {
            exam_id
            for (exam_id,) in db.query(Grade.exam_id).filter(Grade.student_id == actor.id, Grade.exam_id.in_(exam_ids))
        }
    return [
        exam_out(row, attempted=row.id in attempted_ids, has_grade=row.id in graded_ids)
        for row in rows
    ]


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
    try:
        from app.services import ai_engine

        ai_engine.generate_exam_analyses(db, exam, rows)
    except Exception:
        pass
    analyses = _analysis_map(db, exam_id=exam.id)
    return [_grade_out(row, analyses.get((row.exam_id, row.student_id))) for row in rows]


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
    rows = query.order_by(Grade.student_id.asc()).all()
    analyses = _analysis_map(db, exam_id=exam.id)
    return [_grade_out(row, analyses.get((row.exam_id, row.student_id))) for row in rows]


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
    analyses = _analysis_map(db, student_id=student.id)
    return sorted(
        [_grade_out(row, analyses.get((row.exam_id, row.student_id))) for row in rows],
        key=lambda item: item.date,
        reverse=True,
    )


def get_exam_paper(db: Session, exam_id: int, student: User) -> ExamPaperOut:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can take exams")
    exam = get_exam(db, exam_id, student)
    questions = _questions(exam)
    if not questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This exam has no questions yet")
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.student_id == student.id)
        .first()
    )
    grade = db.query(Grade).filter(Grade.exam_id == exam.id, Grade.student_id == student.id).first()
    public = [
        ExamQuestionPublic(prompt=str(item.get("prompt") or ""), options=[str(opt) for opt in item.get("options") or []])
        for item in questions
        if item.get("prompt") and item.get("options")
    ]
    return ExamPaperOut(
        exam_id=exam.id,
        title=exam.title,
        max_marks=exam.max_marks,
        already_attempted=attempt is not None,
        has_grade=grade is not None,
        questions=public if attempt is None and grade is None else [],
    )


def submit_exam_attempt(db: Session, exam_id: int, payload: ExamAttemptRequest, student: User) -> ExamAttemptOut:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can take exams")
    exam = get_exam(db, exam_id, student)
    class_group = load_class(db, exam.class_id)
    from app.services.academic_access import assert_enrolled_in_class

    assert_enrolled_in_class(db, class_group, student)
    existing_attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.student_id == student.id)
        .first()
    )
    if existing_attempt:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already submitted this exam")
    existing_grade = db.query(Grade).filter(Grade.exam_id == exam.id, Grade.student_id == student.id).first()
    if existing_grade:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This exam already has a recorded grade")

    questions = _questions(exam)
    if not questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This exam has no questions yet")
    if len(payload.answers) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Submit one answer for each of the {len(questions)} questions",
        )

    correct_count = 0
    for index, question in enumerate(questions):
        try:
            correct = int(question.get("correct"))
        except (TypeError, ValueError):
            continue
        if payload.answers[index] == correct:
            correct_count += 1
    score = round((correct_count / len(questions)) * exam.max_marks, 1) if questions else 0.0
    attempt = ExamAttempt(
        exam_id=exam.id,
        student_id=student.id,
        answers_json=json.dumps(payload.answers),
        score=score,
    )
    db.add(attempt)
    grade = Grade(exam_id=exam.id, student_id=student.id, marks_obtained=score)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    try:
        from app.services import ai_engine

        row = (
            db.query(Grade)
            .options(
                joinedload(Grade.student),
                joinedload(Grade.exam).joinedload(Exam.class_group).joinedload(ClassGroup.course),
            )
            .filter(Grade.id == grade.id)
            .first()
        )
        if row:
            ai_engine.generate_exam_analyses(db, exam, [row])
    except Exception:
        pass
    percent = round((score / exam.max_marks) * 100, 1) if exam.max_marks else 0.0
    return ExamAttemptOut(
        exam_id=exam.id,
        score=score,
        max_marks=exam.max_marks,
        percent=percent,
        correct_count=correct_count,
        question_count=len(questions),
    )
