from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.public import ContactInfoOut, ContactMessageCreate, ContactMessageOut
from app.services import public as public_service

router = APIRouter(prefix="/contact", tags=["public"])


@router.get("/info", response_model=ContactInfoOut)
def contact_info():
    return public_service.CONTACT_INFO


@router.post("", response_model=ContactMessageOut, status_code=status.HTTP_201_CREATED)
def submit_contact(payload: ContactMessageCreate, db: Session = Depends(get_db)):
    return public_service.create_contact_message(db, payload)
