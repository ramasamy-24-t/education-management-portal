from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.types import EmailAddress
from app.schemas.user import UserPublic


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailAddress
    password: str = Field(min_length=8, max_length=72)
    role: Literal["student", "teacher"]
    school_id: int


class LoginRequest(BaseModel):
    email: EmailAddress
    password: str = Field(min_length=1, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
