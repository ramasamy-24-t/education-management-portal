"""Smoke checks for attendance, assignments, and exams. Run from backend/."""

from datetime import date, datetime, timezone

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
    teacher = token("priya.nair@edu.local")
    other = token("arjun.mehta@edu.local")
    student = token("rohan.sharma@edu.local")

    classes = client.get("/academic/classes", headers=auth(teacher))
    assert classes.status_code == 200 and classes.json(), classes.text
    class_id = classes.json()[0]["id"]

    roster = client.get(f"/academic/classes/{class_id}/students", headers=auth(teacher))
    assert roster.status_code == 200 and roster.json(), roster.text
    student_id = next(row["id"] for row in roster.json() if row["email"] == "rohan.sharma@edu.local")

    marked = client.post(
        "/attendance/mark",
        headers=auth(teacher),
        json={
            "class_id": class_id,
            "date": date.today().isoformat(),
            "records": [{"student_id": student_id, "status": "present"}],
        },
    )
    assert marked.status_code == 200, marked.text

    student_mark = client.post(
        "/attendance/mark",
        headers=auth(student),
        json={
            "class_id": class_id,
            "date": date.today().isoformat(),
            "records": [{"student_id": student_id, "status": "absent"}],
        },
    )
    assert student_mark.status_code == 403

    other_mark = client.post(
        "/attendance/mark",
        headers=auth(other),
        json={
            "class_id": class_id,
            "date": date.today().isoformat(),
            "records": [{"student_id": student_id, "status": "absent"}],
        },
    )
    assert other_mark.status_code == 403

    own = client.get("/attendance", headers=auth(student))
    assert own.status_code == 200
    assert all(row["student_id"] == student_id for row in own.json())

    summary = client.get(f"/attendance/summary?class_id={class_id}", headers=auth(student))
    assert summary.status_code == 200 and len(summary.json()) == 1

    created = client.post(
        "/assignments",
        headers=auth(teacher),
        json={
            "class_id": class_id,
            "title": "Smoke Assignment",
            "description": "Write a short answer.",
            "due_date": datetime.now(timezone.utc).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    assignment_id = created.json()["id"]

    submitted = client.post(
        f"/assignments/{assignment_id}/submissions",
        headers=auth(student),
        json={"content": "My smoke submission."},
    )
    assert submitted.status_code == 201, submitted.text
    submission_id = submitted.json()["id"]

    self_grade = client.patch(
        f"/submissions/{submission_id}",
        headers=auth(student),
        json={"grade": 100, "feedback": "I am great"},
    )
    assert self_grade.status_code == 403

    other_grade = client.patch(
        f"/submissions/{submission_id}",
        headers=auth(other),
        json={"grade": 10, "feedback": "Not my class"},
    )
    assert other_grade.status_code == 403

    graded = client.patch(
        f"/submissions/{submission_id}",
        headers=auth(teacher),
        json={"grade": 88, "feedback": "Good work"},
    )
    assert graded.status_code == 200, graded.text
    assert graded.json()["ai_feedback"]

    exam = client.post(
        "/exams",
        headers=auth(teacher),
        json={"class_id": class_id, "title": "Smoke Exam", "date": date.today().isoformat(), "max_marks": 50},
    )
    assert exam.status_code == 201, exam.text
    exam_id = exam.json()["id"]

    recorded = client.put(
        f"/exams/{exam_id}/grades",
        headers=auth(teacher),
        json={"records": [{"student_id": student_id, "marks_obtained": 41}]},
    )
    assert recorded.status_code == 200, recorded.text
    assert recorded.json()[0]["ai_summary"]
    assert recorded.json()[0]["weak_topics"]

    history = client.get("/grades/me", headers=auth(student))
    assert history.status_code == 200
    assert any(row["exam_id"] == exam_id for row in history.json())

    print("smoke_academic: all checks passed")


if __name__ == "__main__":
    main()
