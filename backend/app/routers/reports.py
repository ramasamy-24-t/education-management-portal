"""Reports & Performance Summary endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.services import reports
from app.services.academic_access import load_class, assert_can_manage_class

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/me")
def my_report(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.student))):
    """Student's own performance report."""
    return reports.student_report(db, user)


@router.get("/student/{student_id}")
def student_report(
    student_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    """Teacher/admin view of a specific student's report."""
    student = db.query(User).filter(User.id == student_id, User.role == UserRole.student).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return reports.student_report(db, student)


@router.get("/class/{class_id}")
def class_report(
    class_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    """Class performance report."""
    class_group = load_class(db, class_id)
    assert_can_manage_class(class_group, user)
    return reports.class_report(db, class_id)


@router.get("/comparative")
def comparative_report(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    """Compare performance across classes."""
    return reports.comparative_report(db, user)


@router.get("/admin/summary")
def admin_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    """Admin insights summary for dashboard."""
    return reports.admin_insights_summary(db)
