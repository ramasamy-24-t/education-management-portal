from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.services import ai_engine, ai_service
from app.services.academic_access import load_class
from app.services.academic_access import assert_can_manage_class

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status")
def ai_status():
    return {"configured": ai_service.is_configured()}


@router.get("/me")
def my_insights(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.student))):
    return ai_engine.list_student_insight_texts(db, user, refresh=True)


@router.post("/refresh")
def refresh_my_insights(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.student))):
    return ai_engine.refresh_student_insights(db, user, force=True)


@router.get("/monitoring")
def monitoring(db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.teacher, UserRole.admin))):
    return {"configured": ai_service.is_configured(), "insights": ai_engine.list_monitoring(db, user)}


@router.post("/monitoring/refresh")
def refresh_monitoring(
    class_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.teacher, UserRole.admin)),
):
    if class_id:
        class_group = load_class(db, class_id)
        assert_can_manage_class(class_group, user)
        ai_engine.refresh_class_insight(db, class_group, force=True)
        return {"refreshed_classes": 1}
    count = ai_engine.refresh_monitoring(db, user)
    return {"refreshed_classes": count}
