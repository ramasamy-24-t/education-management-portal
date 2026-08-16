from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.academic import AttendanceMarkRequest, AttendanceOut, AttendanceSummaryOut
from app.services import attendance as attendance_service

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/mark", response_model=list[AttendanceOut])
def mark(
    payload: AttendanceMarkRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return attendance_service.mark_attendance(db, payload, user)


@router.get("", response_model=list[AttendanceOut])
def list_records(
    class_id: int | None = Query(default=None),
    on_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return attendance_service.list_attendance(db, user, class_id=class_id, on_date=on_date)


@router.get("/summary", response_model=list[AttendanceSummaryOut])
def summary(
    class_id: int = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return attendance_service.attendance_summary(db, user, class_id=class_id)
