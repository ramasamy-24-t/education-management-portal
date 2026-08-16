from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.assignment import Assignment, AssignmentSubmission
from app.models.course import ClassGroup
from app.models.user import User, UserRole
from app.schemas.academic import AssignmentCreate, AssignmentOut, SubmissionCreate, SubmissionGrade, SubmissionOut
from app.services.academic_access import (
    assert_can_manage_class,
    assert_enrolled_in_class,
    can_view_class,
    list_accessible_classes,
    load_class,
)


def _assignment_out(assignment: Assignment) -> AssignmentOut:
    class_group = assignment.class_group
    course = class_group.course if class_group else None
    return AssignmentOut(
        id=assignment.id,
        class_id=assignment.class_id,
        class_name=class_group.name if class_group else "",
        course_title=course.title if course else "",
        title=assignment.title,
        description=assignment.description,
        due_date=assignment.due_date,
    )


def _submission_out(row: AssignmentSubmission) -> SubmissionOut:
    assignment = row.assignment
    return SubmissionOut(
        id=row.id,
        assignment_id=row.assignment_id,
        assignment_title=assignment.title if assignment else "",
        student_id=row.student_id,
        student_name=row.student.name if row.student else "",
        submitted_at=row.submitted_at,
        content=row.content,
        grade=row.grade,
        feedback=row.feedback,
        ai_feedback=row.ai_feedback,
        due_date=assignment.due_date if assignment else None,
    )


def create_assignment(db: Session, payload: AssignmentCreate, actor: User) -> AssignmentOut:
    class_group = load_class(db, payload.class_id)
    assert_can_manage_class(class_group, actor)
    assignment = Assignment(
        class_id=class_group.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        due_date=payload.due_date,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return _assignment_out(assignment)


def list_assignments(db: Session, actor: User, *, class_id: int | None = None) -> list[AssignmentOut]:
    query = db.query(Assignment).options(joinedload(Assignment.class_group).joinedload(ClassGroup.course))
    if class_id:
        class_group = load_class(db, class_id)
        if not can_view_class(db, class_group, actor):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this class")
        query = query.filter(Assignment.class_id == class_id)
    else:
        class_ids = [item.id for item in list_accessible_classes(db, actor)]
        if not class_ids:
            return []
        query = query.filter(Assignment.class_id.in_(class_ids))
    rows = query.order_by(Assignment.due_date.asc()).all()
    return [_assignment_out(row) for row in rows]


def get_assignment(db: Session, assignment_id: int, actor: User) -> Assignment:
    assignment = (
        db.query(Assignment)
        .options(
            joinedload(Assignment.class_group).joinedload(ClassGroup.course),
            joinedload(Assignment.submissions),
        )
        .filter(Assignment.id == assignment_id)
        .first()
    )
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    class_group = load_class(db, assignment.class_id)
    if not can_view_class(db, class_group, actor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this assignment")
    return assignment


def submit_assignment(db: Session, assignment_id: int, payload: SubmissionCreate, student: User) -> SubmissionOut:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can submit assignments")
    assignment = get_assignment(db, assignment_id, student)
    class_group = load_class(db, assignment.class_id)
    assert_enrolled_in_class(db, class_group, student)

    existing = (
        db.query(AssignmentSubmission)
        .filter(
            AssignmentSubmission.assignment_id == assignment.id,
            AssignmentSubmission.student_id == student.id,
        )
        .first()
    )
    if existing and existing.grade is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This submission has already been graded and cannot be changed",
        )
    if existing:
        existing.content = payload.content.strip()
        db.commit()
        db.refresh(existing)
        return _submission_out(existing)

    row = AssignmentSubmission(
        assignment_id=assignment.id,
        student_id=student.id,
        content=payload.content.strip(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _submission_out(row)


def list_submissions(db: Session, assignment_id: int, actor: User) -> list[SubmissionOut]:
    assignment = get_assignment(db, assignment_id, actor)
    class_group = load_class(db, assignment.class_id)
    if actor.role == UserRole.student:
        rows = [row for row in assignment.submissions if row.student_id == actor.id]
    else:
        assert_can_manage_class(class_group, actor)
        rows = list(assignment.submissions)
    return [_submission_out(row) for row in rows]


def grade_submission(db: Session, submission_id: int, payload: SubmissionGrade, actor: User) -> SubmissionOut:
    row = (
        db.query(AssignmentSubmission)
        .options(joinedload(AssignmentSubmission.assignment), joinedload(AssignmentSubmission.student))
        .filter(AssignmentSubmission.id == submission_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    if actor.role == UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Students cannot grade assignments")
    class_group = load_class(db, row.assignment.class_id)
    assert_can_manage_class(class_group, actor)
    row.grade = payload.grade
    row.feedback = payload.feedback.strip()
    db.commit()
    db.refresh(row)
    return _submission_out(row)


def my_submissions(db: Session, student: User) -> list[SubmissionOut]:
    if student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can view their submissions")
    rows = (
        db.query(AssignmentSubmission)
        .options(joinedload(AssignmentSubmission.assignment), joinedload(AssignmentSubmission.student))
        .filter(AssignmentSubmission.student_id == student.id)
        .order_by(AssignmentSubmission.submitted_at.desc())
        .all()
    )
    return [_submission_out(row) for row in rows]
