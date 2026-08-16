from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.dashboard import AdminUserCreate, AdminUserUpdate, ProgressOverviewOut
from app.schemas.user import UserPublic
from app.services import admin_users, dashboard

router = APIRouter(tags=["users"])


@router.get("/users/me/dashboard")
def my_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == UserRole.student:
        return dashboard.student_dashboard(db, user)
    if user.role == UserRole.teacher:
        return dashboard.teacher_dashboard(db, user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No user dashboard for this role")


@router.get("/users/me/progress-overview", response_model=ProgressOverviewOut)
def my_progress(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    return dashboard.student_progress(db, user)


@router.get("/admin/users", response_model=list[UserPublic])
def admin_list_users(
    role: UserRole = Query(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    if role not in (UserRole.student, UserRole.teacher):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role must be student or teacher")
    return admin_users.list_users(db, role=role)


@router.post("/admin/users", response_model=UserPublic, status_code=201)
def admin_create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.admin)),
):
    return admin_users.create_user(db, payload, user)


@router.patch("/admin/users/{user_id}", response_model=UserPublic)
def admin_set_active(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.admin)),
):
    return admin_users.set_active(db, user_id, payload.is_active, user)
