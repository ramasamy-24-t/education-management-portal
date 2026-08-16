from collections import defaultdict, deque
from time import time

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models.user import User, UserRole
from app.services import ai_engine, ai_service
from app.services.academic_access import load_class
from app.services.academic_access import assert_can_manage_class

router = APIRouter(prefix="/ai", tags=["ai"])

_ASSISTANT_HITS: dict[int, deque[float]] = defaultdict(deque)
_ASSISTANT_LIMIT = 12
_ASSISTANT_WINDOW_SECONDS = 300


class PracticeQuestionsRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=300)


class AssistantTurn(BaseModel):
    role: str = Field(max_length=16)
    content: str = Field(max_length=800)


class AssistantRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    history: list[AssistantTurn] = Field(default_factory=list, max_length=8)


def _assistant_rate_limited(student_id: int) -> bool:
    now = time()
    hits = _ASSISTANT_HITS[student_id]
    while hits and now - hits[0] > _ASSISTANT_WINDOW_SECONDS:
        hits.popleft()
    if len(hits) >= _ASSISTANT_LIMIT:
        return True
    hits.append(now)
    return False


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


@router.post("/practice-questions/{student_id}")
def practice_questions(
    student_id: int,
    payload: PracticeQuestionsRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    if user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only generate practice questions for yourself",
        )
    try:
        return ai_engine.generate_practice_questions(db, user, payload.subject)
    except Exception:
        return {
            "subject": payload.subject.strip(),
            "questions": [],
            "source": "error",
            "detail": "Could not generate questions. Try again.",
        }


@router.post("/assistant/{student_id}")
def assistant(
    student_id: int,
    payload: AssistantRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.student)),
):
    if user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only ask the assistant about your own progress",
        )
    if _assistant_rate_limited(user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many questions in a short time. Wait a few minutes and try again.",
        )
    try:
        history = [{"role": turn.role, "content": turn.content} for turn in payload.history]
        return ai_engine.answer_assistant(db, user, payload.question, history)
    except Exception:
        return {
            "answer": "The assistant hit an error. Try a shorter question about your grades or attendance.",
            "source": "error",
        }
