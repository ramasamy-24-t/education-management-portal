from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db_bootstrap import ensure_schema

from app.routers import (
    academic,
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
    teachers,
    users,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_schema()
    yield


app = FastAPI(title="Education Management Portal API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
app.include_router(announcements.router)
app.include_router(faqs.router)
app.include_router(contact.router)
app.include_router(academic.router)
app.include_router(attendance.router)
app.include_router(assignments.router)
app.include_router(exams.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"name": "Education Management Portal API", "docs": "/docs"}
