from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.schemas.public import ContactInfoOut, ContactMessageCreate, ContactMessageOut
from app.services import public as public_service

router = APIRouter(prefix="/contact", tags=["public"])


@router.get("/info", response_model=ContactInfoOut)
def contact_info():
    return public_service.CONTACT_INFO


@router.get("/messages", response_model=list[ContactMessageOut])
def list_messages(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
):
    return public_service.list_contact_messages(db)


@router.post("", response_model=ContactMessageOut, status_code=status.HTTP_201_CREATED)
def submit_contact(payload: ContactMessageCreate, db: Session = Depends(get_db)):
    return public_service.create_contact_message(db, payload)
