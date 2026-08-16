from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.types import EmailAddress


class AnnouncementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    created_at: datetime


class FAQOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str
    answer: str


class ContactMessageCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailAddress
    message: str = Field(min_length=10, max_length=4000)


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailAddress
    message: str
    created_at: datetime


class ContactInfoOut(BaseModel):
    organization: str
    email: str
    phone: str
    address: str
    hours: str
    support_email: str
    support_note: str
