from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=80)
    schedule: str = Field(min_length=1, max_length=255)
    syllabus: str = ""
    teacher_id: int | None = None
    rating: float | None = Field(default=None, ge=0, le=5)


class CourseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    category: str | None = Field(default=None, min_length=1, max_length=80)
    schedule: str | None = Field(default=None, min_length=1, max_length=255)
    syllabus: str | None = None
    teacher_id: int | None = None
    rating: float | None = Field(default=None, ge=0, le=5)


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    category: str
    teacher_id: int
    teacher_name: str
    schedule: str
    rating: float
    syllabus: str
    class_count: int = 0
    enrollment_count: int = 0
    enrolled: bool = False


class ClassCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class ClassUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class ClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    name: str
