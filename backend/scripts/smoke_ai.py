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

    student = token("rohan.sharma@edu.local")
    admin = token("admin@edu.local", admin=True)

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

    print("smoke_ai: all checks passed")


if __name__ == "__main__":
    main()
