from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.academic import ExamCreate, ExamGradesRequest, ExamOut, GradeOut
from app.services import exams as exam_service

router = APIRouter(tags=["exams"])


@router.post("/exams", response_model=ExamOut, status_code=201)
def create_exam(
    payload: ExamCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return exam_service.create_exam(db, payload, user)


@router.get("/exams", response_model=list[ExamOut])
def list_exams(
    class_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return exam_service.list_exams(db, user, class_id=class_id)


@router.get("/exams/{exam_id}", response_model=ExamOut)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return exam_service._exam_out(exam_service.get_exam(db, exam_id, user))


@router.put("/exams/{exam_id}/grades", response_model=list[GradeOut])
def record_grades(
    exam_id: int,
    payload: ExamGradesRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return exam_service.record_grades(db, exam_id, payload, user)


@router.get("/exams/{exam_id}/grades", response_model=list[GradeOut])
def list_grades(
    exam_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return exam_service.list_exam_grades(db, exam_id, user)


@router.get("/grades/me", response_model=list[GradeOut])
def my_grades(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return exam_service.my_grade_history(db, user)
