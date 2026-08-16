from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.attendance import AttendanceStatus


class ClassContextOut(BaseModel):
    id: int
    name: str
    course_id: int
    course_title: str
    teacher_id: int


class RosterStudentOut(BaseModel):
    id: int
    name: str
    email: str


class AttendanceRecordIn(BaseModel):
    student_id: int
    status: AttendanceStatus


class AttendanceMarkRequest(BaseModel):
    class_id: int
    date: date
    records: list[AttendanceRecordIn] = Field(min_length=1)


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    student_name: str
    class_id: int
    class_name: str
    course_title: str
    date: date
    status: AttendanceStatus


class AttendanceSummaryOut(BaseModel):
    student_id: int
    student_name: str
    class_id: int
    class_name: str
    present: int
    late: int
    absent: int
    total: int
    percent_present: float


class AssignmentCreate(BaseModel):
    class_id: int
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=1)
    due_date: datetime


class AssignmentOut(BaseModel):
    id: int
    class_id: int
    class_name: str
    course_title: str
    title: str
    description: str
    due_date: datetime


class SubmissionCreate(BaseModel):
    content: str = Field(min_length=1)


class SubmissionGrade(BaseModel):
    grade: float = Field(ge=0, le=100)
    feedback: str = Field(min_length=1)


class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    assignment_title: str
    student_id: int
    student_name: str
    submitted_at: datetime
    content: str
    grade: float | None
    feedback: str | None
    ai_feedback: str | None
    due_date: datetime | None = None


class ExamCreate(BaseModel):
    class_id: int
    title: str = Field(min_length=2, max_length=200)
    date: date
    max_marks: float = Field(gt=0)


class ExamOut(BaseModel):
    id: int
    class_id: int
    class_name: str
    course_title: str
    title: str
    date: date
    max_marks: float


class GradeRecordIn(BaseModel):
    student_id: int
    marks_obtained: float = Field(ge=0)


class ExamGradesRequest(BaseModel):
    records: list[GradeRecordIn] = Field(min_length=1)


class GradeOut(BaseModel):
    id: int
    exam_id: int
    exam_title: str
    student_id: int
    student_name: str
    class_name: str
    course_title: str
    date: date
    max_marks: float
    marks_obtained: float
    percent: float
    ai_summary: str | None = None
    weak_topics: str | None = None
