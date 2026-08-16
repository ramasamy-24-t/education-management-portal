from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import TeacherPublic, UserPublic
from app.services import teachers as teacher_service

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/top", response_model=list[TeacherPublic])
def top_teachers(limit: int = Query(default=5, ge=1, le=20), db: Session = Depends(get_db)):
    return teacher_service.top_teachers(db, limit=limit)


@router.get("", response_model=list[UserPublic])
def list_teachers(db: Session = Depends(get_db)):
    return teacher_service.list_teachers(db)
