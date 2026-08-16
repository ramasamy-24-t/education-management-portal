"""Smoke checks for dashboards and admin user management."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def token(email: str, admin: bool = False) -> str:
    path = "/auth/admin/login" if admin else "/auth/login"
    response = client.post(path, json={"email": email, "password": "password123"})
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def auth(value: str) -> dict:
    return {"Authorization": f"Bearer {value}"}


def main() -> None:
    student = token("rohan.sharma@edu.example.com")
    teacher = token("priya.nair@edu.example.com")
    admin = token("admin@edu.example.com", admin=True)

    student_dash = client.get("/users/me/dashboard", headers=auth(student))
    assert student_dash.status_code == 200, student_dash.text
    body = student_dash.json()
    assert body["profile"]["role"] == "student"
    assert "progress_overview" in body
    assert isinstance(body["ai_recommendations"], list)

    progress = client.get("/users/me/progress-overview", headers=auth(student))
    assert progress.status_code == 200, progress.text
    overview = progress.json()
    assert "weak_subjects" in overview and "improvement_tips" in overview and "ai_insights" in overview

    teacher_progress = client.get("/users/me/progress-overview", headers=auth(teacher))
    assert teacher_progress.status_code == 403

    teacher_dash = client.get("/users/me/dashboard", headers=auth(teacher))
    assert teacher_dash.status_code == 200
    assert teacher_dash.json()["classes"]

    email = f"temp.student.{uuid4().hex[:8]}@edu.example.com"
    created = client.post(
        "/admin/users",
        headers=auth(admin),
        json={
            "name": "Temp Student",
            "email": email,
            "password": "password123",
            "role": "student",
        },
    )
    assert created.status_code == 201, created.text
    user_id = created.json()["id"]

    forbidden = client.post(
        "/admin/users",
        headers=auth(teacher),
        json={"name": "Nope", "email": "nope@edu.example.com", "password": "password123", "role": "student"},
    )
    assert forbidden.status_code == 403

    deactivated = client.patch(f"/admin/users/{user_id}", headers=auth(admin), json={"is_active": False})
    assert deactivated.status_code == 200 and deactivated.json()["is_active"] is False

    blocked = client.post("/auth/login", json={"email": email, "password": "password123"})
    assert blocked.status_code == 403

    client.patch(f"/admin/users/{user_id}", headers=auth(admin), json={"is_active": True})

    messages = client.get("/contact/messages", headers=auth(admin))
    assert messages.status_code == 200, messages.text
    student_mail = client.get("/contact/messages", headers=auth(student))
    assert student_mail.status_code == 403

    students = client.get("/admin/users?role=student", headers=auth(admin))
    assert students.status_code == 200
    rohan = next(row for row in students.json() if row["email"].startswith("rohan.sharma"))
    kavya = token("kavya.reddy@edu.example.com")
    blocked_report = client.get(f"/reports/student/{rohan['id']}", headers=auth(kavya))
    assert blocked_report.status_code == 403, blocked_report.text
    allowed_report = client.get(f"/reports/student/{rohan['id']}", headers=auth(teacher))
    assert allowed_report.status_code == 200, allowed_report.text

    print("smoke_dashboards: all checks passed")


if __name__ == "__main__":
    main()
