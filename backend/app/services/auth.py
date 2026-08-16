from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.constants import DEMO_EMAIL_DOMAIN
from app.models.school import School
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.security import create_access_token, hash_password, verify_password


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    school = db.get(School, payload.school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Select a valid school")
    user = User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        role=UserRole(payload.role),
        school_id=school.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _email_candidates(email: str) -> list[str]:
    cleaned = str(email or "").strip().lower()
    candidates = [cleaned]
    if cleaned.endswith("@edu.local"):
        candidates.append(cleaned.replace("@edu.local", f"@{DEMO_EMAIL_DOMAIN}", 1))
    elif cleaned.endswith(f"@{DEMO_EMAIL_DOMAIN}"):
        candidates.append(cleaned.replace(f"@{DEMO_EMAIL_DOMAIN}", "@edu.local", 1))
    return candidates


def authenticate(db: Session, payload: LoginRequest, *, allowed_roles: list[UserRole]) -> User:
    candidates = _email_candidates(payload.email)
    user = db.query(User).filter(User.email.in_(candidates)).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
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
