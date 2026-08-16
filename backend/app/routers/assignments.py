from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.academic import (
    AssignmentCreate,
    AssignmentOut,
    SubmissionGrade,
    SubmissionOut,
)
from app.services import assignments as assignment_service

router = APIRouter(tags=["assignments"])


@router.post("/assignments", response_model=AssignmentOut, status_code=201)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return assignment_service.create_assignment(db, payload, user)


@router.get("/assignments", response_model=list[AssignmentOut])
def list_assignments(
    class_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return assignment_service.list_assignments(db, user, class_id=class_id)


@router.get("/assignments/{assignment_id}", response_model=AssignmentOut)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return assignment_service.assignment_out(assignment_service.get_assignment(db, assignment_id, user))


@router.post("/assignments/{assignment_id}/submissions", response_model=SubmissionOut, status_code=201)
def submit_assignment(
    assignment_id: int,
    content: str = Form(default=""),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return assignment_service.submit_assignment(db, assignment_id, user, content=content, upload=file)


@router.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionOut])
def list_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return assignment_service.list_submissions(db, assignment_id, user)


@router.patch("/submissions/{submission_id}", response_model=SubmissionOut)
def grade_submission(
    submission_id: int,
    payload: SubmissionGrade,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return assignment_service.grade_submission(db, submission_id, payload, user)


@router.get("/submissions/me", response_model=list[SubmissionOut])
def my_submissions(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return assignment_service.my_submissions(db, user)


@router.get("/submissions/{submission_id}/file")
def download_submission_file(
    submission_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    path, filename = assignment_service.get_submission_file(db, submission_id, user)
    return FileResponse(path, filename=filename)
