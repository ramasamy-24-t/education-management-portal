from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.dashboard import AdminUserCreate
from app.schemas.user import UserPublic
from app.services.security import hash_password


def list_users(db: Session, *, role: UserRole) -> list[UserPublic]:
    rows = db.query(User).filter(User.role == role).order_by(User.name.asc()).all()
    return [UserPublic.model_validate(row) for row in rows]


def create_user(db: Session, payload: AdminUserCreate, actor: User) -> UserPublic:
    if actor.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    if payload.role not in (UserRole.student.value, UserRole.teacher.value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin can only create students or teachers")
    email = str(payload.email)
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)


def set_active(db: Session, user_id: int, is_active: bool, actor: User) -> UserPublic:
    if actor.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.role == UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin accounts cannot be deactivated here")
    if user.id == actor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot deactivate your own account")
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)
