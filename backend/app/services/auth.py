from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.security import create_access_token, hash_password, verify_password


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, payload: LoginRequest, *, allowed_roles: list[UserRole]) -> User:
    user = db.query(User).filter(User.email == str(payload.email).lower()).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if user.role not in allowed_roles:
        if user.role == UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin accounts must sign in through Admin Login",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Use the student/teacher login page for this account",
        )
    return user


def issue_token(user: User) -> str:
    return create_access_token(user_id=user.id, role=user.role.value)
