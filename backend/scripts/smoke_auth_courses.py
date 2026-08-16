"""Quick smoke checks for auth + course ownership. Run from backend/: python scripts/smoke_auth_courses.py"""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def main() -> None:
    student = client.post("/auth/login", json={"email": "rohan.sharma@edu.example.com", "password": "password123"})
    assert student.status_code == 200, student.text
    student_token = student.json()["access_token"]

    admin_on_user = client.post("/auth/login", json={"email": "admin@edu.example.com", "password": "password123"})
    assert admin_on_user.status_code == 403, admin_on_user.text

    admin = client.post("/auth/admin/login", json={"email": "admin@edu.example.com", "password": "password123"})
    assert admin.status_code == 200, admin.text

    teacher = client.post("/auth/login", json={"email": "priya.nair@edu.example.com", "password": "password123"})
    other = client.post("/auth/login", json={"email": "arjun.mehta@edu.example.com", "password": "password123"})
    assert teacher.status_code == 200 and other.status_code == 200
    teacher_token = teacher.json()["access_token"]
    other_token = other.json()["access_token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {student_token}"})
    assert me.status_code == 200 and me.json()["role"] == "student"

    created = client.post(
        "/courses",
        json={
            "title": "Smoke Test Course",
            "description": "Temporary course for ownership checks",
            "category": "Computer Science",
            "schedule": "Mon 09:00",
            "syllabus": "1. Intro",
        },
        headers={"Authorization": f"Bearer {teacher_token}"},
    )
    assert created.status_code == 201, created.text
    course_id = created.json()["id"]

    forbidden = client.patch(
        f"/courses/{course_id}",
        json={"title": "Hijacked"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert forbidden.status_code == 403, forbidden.text

    student_create = client.post(
        "/courses",
        json={
            "title": "Nope",
            "description": "Students cannot create",
            "category": "X",
            "schedule": "Tue",
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_create.status_code == 403

    enroll = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert enroll.status_code == 201, enroll.text

    teacher_enroll = client.post(
        "/enrollments",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {teacher_token}"},
    )
    assert teacher_enroll.status_code == 403

    top = client.get("/courses/top-rated")
    assert top.status_code == 200 and len(top.json()) >= 1

    teachers = client.get("/teachers/top")
    assert teachers.status_code == 200 and len(teachers.json()) >= 1

    deleted = client.delete(f"/courses/{course_id}", headers={"Authorization": f"Bearer {teacher_token}"})
    assert deleted.status_code == 204, deleted.text

    schools = client.get("/schools")
    assert schools.status_code == 200 and schools.json()
    school_id = schools.json()[0]["id"]
    email = f"register.smoke.{uuid4().hex[:10]}@edu.example.com"
    registered = client.post(
        "/auth/register",
        json={
            "name": "Register Smoke",
            "email": email,
            "password": "password123",
            "role": "student",
            "school_id": school_id,
        },
    )
    assert registered.status_code == 201, registered.text
    assert registered.json().get("access_token")
    signed_in = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert signed_in.status_code == 200, signed_in.text

    print("smoke_auth_courses: all checks passed")


if __name__ == "__main__":
    main()
