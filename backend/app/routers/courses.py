from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_optional_user, require_roles
from app.models.user import User, UserRole
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate
from app.services import courses as course_service

router = APIRouter(prefix="/courses", tags=["courses"])


def _student_id(user: User | None) -> int | None:
    if user and user.role == UserRole.student:
        return user.id
    return None


@router.get("", response_model=list[CourseOut])
def list_courses(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    teacher_id: int | None = Query(default=None),
    sort: str | None = Query(default=None, description="Use 'rating' for top-rated order"),
    limit: int | None = Query(default=None, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    return course_service.list_courses(
        db,
        search=search,
        category=category,
        teacher_id=teacher_id,
        sort=sort,
        limit=limit,
        student_id=_student_id(user),
    )


@router.get("/top-rated", response_model=list[CourseOut])
def top_rated(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    return course_service.list_courses(db, sort="rating", limit=limit, student_id=_student_id(user))


@router.get("/categories", response_model=list[str])
def categories(db: Session = Depends(get_db)):
    return course_service.list_categories(db)


@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    return course_service.get_course(db, course_id, student_id=_student_id(user))


@router.post("", response_model=CourseOut, status_code=201)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return course_service.create_course(db, payload, user)


@router.patch("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    return course_service.update_course(db, course_id, payload, user)


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    course_service.delete_course(db, course_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
