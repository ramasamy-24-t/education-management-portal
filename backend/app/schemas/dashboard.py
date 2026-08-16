from pydantic import BaseModel, Field

from app.schemas.types import EmailAddress
from app.schemas.academic import (
    AssignmentOut,
    AttendanceSummaryOut,
    ClassContextOut,
    GradeOut,
    SubmissionOut,
)
from app.schemas.course import CourseOut
from app.schemas.user import UserPublic


class AssignmentWithSubmission(AssignmentOut):
    my_submission: SubmissionOut | None = None


class ProgressOverviewOut(BaseModel):
    attendance_percent: float
    average_exam_percent: float
    assignments_submitted: int
    assignments_total: int
    assignment_completion_percent: float
    average_assignment_grade: float | None = None
    course_count: int
    weak_subjects: list[str] = Field(default_factory=list)
    improvement_tips: list[str] = Field(default_factory=list)
    ai_insights: list[str] = Field(default_factory=list)
    ai_pending: bool = True
    risk_trend: str | None = None
    risk_trend_reason: str | None = None


class StudentDashboardOut(BaseModel):
    profile: UserPublic
    courses: list[CourseOut]
    assignments: list[AssignmentWithSubmission]
    attendance: list[AttendanceSummaryOut]
    grades: list[GradeOut]
    progress_overview: ProgressOverviewOut
    ai_recommendations: list[str] = Field(default_factory=list)


class TeacherDashboardOut(BaseModel):
    profile: UserPublic
    courses: list[CourseOut]
    classes: list[ClassContextOut]


class AdminUserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailAddress
    password: str = Field(min_length=8, max_length=72)
    role: str


class AdminUserUpdate(BaseModel):
    is_active: bool
