from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.academic import ClassContextOut, RosterStudentOut
from app.services.academic_access import can_view_class, enrolled_students, list_accessible_classes, load_class

router = APIRouter(prefix="/academic", tags=["academic"])


@router.get("/classes", response_model=list[ClassContextOut])
def my_classes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = list_accessible_classes(db, user)
    return [
        ClassContextOut(
            id=row.id,
            name=row.name,
            course_id=row.course_id,
            course_title=row.course.title if row.course else "",
            teacher_id=row.course.teacher_id if row.course else 0,
        )
        for row in rows
    ]


@router.get("/classes/{class_id}/students", response_model=list[RosterStudentOut])
def class_roster(class_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    class_group = load_class(db, class_id)
    if not can_view_class(db, class_group, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this class")
    return [RosterStudentOut(id=student.id, name=student.name, email=student.email) for student in enrolled_students(db, class_group)]
