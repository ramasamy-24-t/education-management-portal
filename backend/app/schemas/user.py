from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.user import UserRole
from app.schemas.types import EmailAddress


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailAddress
    role: UserRole
    is_active: bool = True
    school_id: int | None = None
    created_at: datetime


class TeacherPublic(UserPublic):
    average_rating: float = 0.0
    course_count: int = 0
    student_count: int = 0
