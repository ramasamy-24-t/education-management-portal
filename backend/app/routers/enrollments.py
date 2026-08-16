from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.services import enrollments as enrollment_service

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("", response_model=EnrollmentOut, status_code=201)
def enroll(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return enrollment_service.enroll_student(db, payload.course_id, user)


@router.get("/me", response_model=list[EnrollmentOut])
def my_enrollments(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return enrollment_service.list_my_enrollments(db, user)
