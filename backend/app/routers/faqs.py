from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.public import FAQOut
from app.services import public as public_service

router = APIRouter(prefix="/faqs", tags=["public"])


@router.get("", response_model=list[FAQOut])
def list_faqs(db: Session = Depends(get_db)):
    return public_service.list_faqs(db)
