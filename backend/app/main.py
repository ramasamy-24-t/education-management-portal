from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db_bootstrap import ensure_schema
from app.services.uploads import ensure_upload_dir

from app.routers import (
    academic,
    ai,
    announcements,
    assignments,
    attendance,
    auth,
    classes,
    contact,
    courses,
    enrollments,
    exams,
    faqs,
    health,
    reports,
    schools,
    teachers,
    users,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_schema()
    ensure_upload_dir()
    yield


app = FastAPI(title="Education Management Portal API", version="0.1.0", lifespan=lifespan)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(classes.router)
app.include_router(enrollments.router)
app.include_router(teachers.router)
app.include_router(schools.router)
app.include_router(announcements.router)
app.include_router(faqs.router)
app.include_router(contact.router)
app.include_router(academic.router)
app.include_router(attendance.router)
app.include_router(assignments.router)
app.include_router(exams.router)
app.include_router(users.router)
app.include_router(ai.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"name": "Education Management Portal API", "docs": "/docs"}
