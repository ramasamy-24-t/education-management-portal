"""AI Engine smoke: pages stay up even if Azure fails."""

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
    from app.db_bootstrap import ensure_schema

    ensure_schema()

    status = client.get("/ai/status")
    assert status.status_code == 200
    assert "configured" in status.json()

    student = token("rohan.sharma@edu.example.com")
    admin = token("admin@edu.example.com", admin=True)

    progress = client.get("/users/me/progress-overview", headers=auth(student))
    assert progress.status_code == 200, progress.text
    body = progress.json()
    assert "weak_subjects" in body
    assert "improvement_tips" in body
    assert "ai_insights" in body
    assert "risk_trend" in body
    assert body["risk_trend"] in (None, "improving", "worsening", "stable")
    assert "risk_trend_reason" in body

    denied = client.get("/ai/monitoring", headers=auth(student))
    assert denied.status_code == 403

    monitoring = client.get("/ai/monitoring", headers=auth(admin))
    assert monitoring.status_code == 200, monitoring.text
    assert "insights" in monitoring.json()

    refreshed = client.post("/ai/refresh", headers=auth(student))
    assert refreshed.status_code == 200, refreshed.text
    payload = refreshed.json()
    assert payload.get("performance")
    assert payload.get("weak_subject")
    assert payload.get("recommendation")
    assert "trend" in payload
    assert payload["trend"] in (None, "improving", "worsening", "stable")
    assert payload.get("trend_reason")

    from app.services import ai_service

    if ai_service.is_configured():
        sample = ai_service.complete("Reply with the single word OK")
        assert sample is None or "OK" in sample.upper()

    me = client.get("/auth/me", headers=auth(student))
    assert me.status_code == 200
    student_id = me.json()["id"]
    practice = client.post(
        f"/ai/practice-questions/{student_id}",
        headers=auth(student),
        json={"subject": "Linear Algebra"},
    )
    assert practice.status_code == 200, practice.text
    practice_body = practice.json()
    assert isinstance(practice_body.get("questions"), list)
    assert practice_body.get("source") in ("model", "fallback", "error")

    other = client.post(
        "/ai/practice-questions/99999",
        headers=auth(student),
        json={"subject": "Linear Algebra"},
    )
    assert other.status_code == 403

    admin_denied = client.post(
        f"/ai/practice-questions/{student_id}",
        headers=auth(admin),
        json={"subject": "Linear Algebra"},
    )
    assert admin_denied.status_code == 403

    chat = client.post(
        f"/ai/assistant/{student_id}",
        headers=auth(student),
        json={"question": "What should I study first given my grades?"},
    )
    assert chat.status_code == 200, chat.text
    assert isinstance(chat.json().get("answer"), str) and chat.json()["answer"]

    other_chat = client.post(
        "/ai/assistant/99999",
        headers=auth(student),
        json={"question": "How is the other student doing?"},
    )
    assert other_chat.status_code == 403

    saved_practice = client.get(f"/ai/practice-questions/{student_id}", headers=auth(student))
    assert saved_practice.status_code == 200
    assert any(item["subject"] == "Linear Algebra" for item in saved_practice.json().get("sets", []))

    saved_chat = client.get(f"/ai/assistant/{student_id}", headers=auth(student))
    assert saved_chat.status_code == 200
    assert saved_chat.json().get("messages")

    tips = client.get("/ai/study-tips")
    assert tips.status_code == 200
    assert len(tips.json().get("tips") or []) >= 3

    denied_tips = client.post("/ai/study-tips/refresh")
    assert denied_tips.status_code == 401
    refreshed_tips = client.post("/ai/study-tips/refresh", headers=auth(admin))
    assert refreshed_tips.status_code == 200, refreshed_tips.text
    assert len(refreshed_tips.json().get("tips") or []) >= 3

    print("smoke_ai: all checks passed")


if __name__ == "__main__":
    main()
