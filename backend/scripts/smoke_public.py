"""Smoke checks for public Home/Contact APIs. Run from backend/: python scripts/smoke_public.py"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def main() -> None:
    announcements = client.get("/announcements")
    assert announcements.status_code == 200, announcements.text
    assert len(announcements.json()) >= 1

    faqs = client.get("/faqs")
    assert faqs.status_code == 200 and len(faqs.json()) >= 1, faqs.text

    info = client.get("/contact/info")
    assert info.status_code == 200
    assert info.json()["support_email"] == "support@edu.example.com"

    created = client.post(
        "/contact",
        json={
            "name": "Smoke Visitor",
            "email": "visitor@example.com",
            "message": "This is a smoke-test contact message.",
        },
    )
    assert created.status_code == 201, created.text

    featured = client.get("/courses/top-rated?limit=4")
    teachers = client.get("/teachers/top?limit=3")
    assert featured.status_code == 200 and teachers.status_code == 200

    schools = client.get("/schools")
    assert schools.status_code == 200 and len(schools.json()) >= 2

    print("smoke_public: all checks passed")


if __name__ == "__main__":
    main()
