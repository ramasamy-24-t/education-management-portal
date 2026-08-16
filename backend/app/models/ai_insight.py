from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InsightType(str, PyEnum):
    performance = "performance"
    at_risk = "at_risk"
    weak_subject = "weak_subject"
    recommendation = "recommendation"
    class_insight = "class_insight"


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    class_id: Mapped[int | None] = mapped_column(ForeignKey("classes.id"), nullable=True, index=True)
    type: Mapped[InsightType] = mapped_column(Enum(InsightType), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student = relationship("User", back_populates="ai_insights")
    class_group = relationship("ClassGroup", back_populates="ai_insights")
