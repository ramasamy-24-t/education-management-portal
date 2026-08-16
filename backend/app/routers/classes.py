from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.schemas.course import ClassCreate, ClassOut, ClassUpdate
from app.services import classes as class_service

router = APIRouter(tags=["classes"])


@router.get("/courses/{course_id}/classes", response_model=list[ClassOut])
def list_classes(course_id: int, db: Session = Depends(get_db)):
    return class_service.list_classes(db, course_id)


@router.post("/courses/{course_id}/classes", response_model=ClassOut, status_code=201)
def create_class(
    course_id: int,
    payload: ClassCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return class_service.create_class(db, course_id, payload, user)


@router.patch("/classes/{class_id}", response_model=ClassOut)
def update_class(
    class_id: int,
    payload: ClassUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return class_service.update_class(db, class_id, payload, user)


@router.delete("/classes/{class_id}", status_code=204)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    class_service.delete_class(db, class_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
