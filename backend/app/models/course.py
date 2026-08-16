from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    school_id: Mapped[int | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    schedule: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    syllabus: Mapped[str] = mapped_column(Text, nullable=False, default="")

    teacher = relationship("User", back_populates="taught_courses")
    school = relationship("School", back_populates="courses")
    classes = relationship("ClassGroup", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")


class ClassGroup(Base):
    """A class section belonging to a course (table name: classes)."""

    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    course = relationship("Course", back_populates="classes")
    attendance_records = relationship("Attendance", back_populates="class_group")
    assignments = relationship("Assignment", back_populates="class_group")
    exams = relationship("Exam", back_populates="class_group")
    ai_insights = relationship("AIInsight", back_populates="class_group")
