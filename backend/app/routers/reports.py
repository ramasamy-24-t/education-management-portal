"""Reports & Performance Summary endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.services import reports
from app.services.academic_access import assert_can_manage_class, assert_can_view_student_report, load_class

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/me")
def my_report(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.student))):
    """Student's own performance report."""
    return reports.student_report(db, user)


@router.get("/me/pdf")
def my_report_pdf(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.student))):
    content = reports.student_report_pdf(db, user)
    filename = f"performance-report-{user.id}.pdf"
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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
    assert_can_view_student_report(db, user, student)
    return reports.student_report(db, student)


@router.get("/student/{student_id}/pdf")
def student_report_pdf(
    student_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    student = db.query(User).filter(User.id == student_id, User.role == UserRole.student).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    assert_can_view_student_report(db, user, student)
    content = reports.student_report_pdf(db, student)
    filename = f"performance-report-{student.id}.pdf"
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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
