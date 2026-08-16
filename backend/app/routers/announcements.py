from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.public import AnnouncementOut
from app.services import public as public_service

router = APIRouter(prefix="/announcements", tags=["public"])


@router.get("", response_model=list[AnnouncementOut])
def list_announcements(limit: int = Query(default=8, ge=1, le=50), db: Session = Depends(get_db)):
    return public_service.list_announcements(db, limit=limit)
