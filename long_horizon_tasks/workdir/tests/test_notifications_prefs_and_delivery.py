from fastapi.testclient import TestClient

from app.main import app


def _signup_and_login(client: TestClient, email: str) -> str:
    client.post(
        "/auth/signup",
        json={
            "name": "User",
            "email": email,
            "password": "supersecret",
            "contact": email,
            "area": "zone",
        },
    )
    r = client.post("/auth/login", json={"email": email, "password": "supersecret"})
    return r.json()["token"]


def test_member_updates_notification_preferences_and_applies_to_future_notifications():
    client = TestClient(app)
    token = _signup_and_login(client, "prefs@example.com")

    # turn off new request notifications
    r = client.patch(
        "/notifications/prefs",
        headers={"Authorization": f"Bearer {token}"},
        json={"on_new_request": False},
    )
    assert r.status_code == 200
    assert r.json()["on_new_request"] is False

    # create another member who creates a request
    token_req = _signup_and_login(client, "req2@example.com")
    r = client.post(
        "/time-bank/requests",
        headers={"Authorization": f"Bearer {token_req}"},
        json={
            "category": "errands",
            "description": "Need groceries",
            "estimated_hours": 1.0,
            "preferred_time": "today",
        },
    )
    assert r.status_code == 200

    # ensure the opted-out member did not receive a new_help_request notification
    from app.storage.db import db_session

    with db_session() as conn:
        member = conn.execute(
            "SELECT m.id AS id FROM members m JOIN users u ON u.id = m.user_id WHERE u.email = ?",
            ("prefs@example.com",),
        ).fetchone()["id"]
        count = conn.execute(
            "SELECT COUNT(*) AS c FROM notifications WHERE member_id = ? AND event_type = 'new_help_request'",
            (member,),
        ).fetchone()["c"]
        assert count == 0


def test_notification_delivery_failure_is_recorded_and_not_retried_excessively():
    client = TestClient(app)
    token = _signup_and_login(client, "deliv@example.com")

    # create a request to generate notifications
    r = client.post(
        "/time-bank/requests",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "category": "rides",
            "description": "Ride needed",
            "estimated_hours": 1.0,
            "preferred_time": "soon",
        },
    )
    assert r.status_code == 200

    from app.storage.db import db_session

    with db_session() as conn:
        member_id = conn.execute(
            "SELECT m.id AS id FROM members m JOIN users u ON u.id = m.user_id WHERE u.email = ?",
            ("deliv@example.com",),
        ).fetchone()["id"]
        notif_row = conn.execute(
            "SELECT id FROM notifications WHERE member_id = ? ORDER BY created_at DESC LIMIT 1",
            (member_id,),
        ).fetchone()
        assert notif_row is not None
        notif_id = notif_row["id"]

    # record failure
    r = client.post(
        "/notifications/deliver",
        headers={"Authorization": f"Bearer {token}"},
        json={"notification_id": notif_id, "status": "failed", "failure_reason": "bounce"},
    )
    assert r.status_code == 200

    # attempt to deliver again - should be a no-op (status stays failed)
    r = client.post(
        "/notifications/deliver",
        headers={"Authorization": f"Bearer {token}"},
        json={"notification_id": notif_id, "status": "failed", "failure_reason": "bounce"},
    )
    assert r.status_code == 200

    with db_session() as conn:
        row = conn.execute("SELECT status, failure_reason FROM notifications WHERE id = ?", (notif_id,)).fetchone()
        assert row["status"] == "failed"
        assert row["failure_reason"] == "bounce"
