from datetime import date as date_type, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    max_marks: Mapped[float] = mapped_column(Float, nullable=False)
    questions_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    class_group = relationship("ClassGroup", back_populates="exams")
    grades = relationship("Grade", back_populates="exam")
    analyses = relationship("ExamAnalysis", back_populates="exam")
    attempts = relationship("ExamAttempt", back_populates="exam")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    marks_obtained: Mapped[float] = mapped_column(Float, nullable=False)

    exam = relationship("Exam", back_populates="grades")
    student = relationship("User", back_populates="grades")


class ExamAnalysis(Base):
    __tablename__ = "exam_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False, index=True)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=False)
    weak_topics: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student = relationship("User", back_populates="exam_analyses")
    exam = relationship("Exam", back_populates="analyses")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    __table_args__ = (UniqueConstraint("exam_id", "student_id", name="uq_exam_attempt_student"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    answers_json: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    exam = relationship("Exam", back_populates="attempts")
    student = relationship("User", back_populates="exam_attempts")
