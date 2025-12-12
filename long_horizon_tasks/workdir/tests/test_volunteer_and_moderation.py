from fastapi.testclient import TestClient

from app.main import app


def _signup_and_login(client: TestClient, email: str) -> tuple[str, str, str]:
    # returns (token, user_id, member_id)
    r = client.post(
        "/auth/signup",
        json={
            "name": "User",
            "email": email,
            "password": "supersecret",
            "contact": email,
            "area": "zone",
        },
    )
    user_id = r.json()["user_id"]
    member_id = r.json()["member_id"]
    r = client.post("/auth/login", json={"email": email, "password": "supersecret"})
    return r.json()["token"], user_id, member_id


def test_member_volunteers_into_community_bank_increases_pool_balance():
    client = TestClient(app)
    token, _, member_id = _signup_and_login(client, "vol@example.com")

    # Capture starting pool balance (may be pre-seeded by other tests in this session DB)
    r = client.get(
        "/time-bank/balances/community_bank/pool",
        headers={"Authorization": f"Bearer {token}"},
    )
    start = r.json()["hours"]

    r = client.post(
        "/time-bank/help-sessions",
        headers={"Authorization": f"Bearer {token}"},
        json={"helper_member_id": member_id, "recipient_member_id": member_id},
    )
    session_id = r.json()["session_id"]

    r = client.post(
        f"/time-bank/help-sessions/{session_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
        json={"agreed_hours": 3.0, "funding_source": "volunteer"},
    )
    assert r.status_code == 200

    r = client.get(
        "/time-bank/balances/community_bank/pool",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.json()["hours"] == start + 3.0


def test_member_reports_and_moderator_can_resolve_report():
    client = TestClient(app)

    reporter_token, _, reporter_member = _signup_and_login(client, "rep@example.com")
    mod_token, mod_user, mod_member = _signup_and_login(client, "mod@example.com")

    # Promote moderator in DB
    from app.storage.db import db_session

    with db_session() as conn:
        conn.execute("UPDATE user_roles SET role = 'moderator' WHERE user_id = ?", (mod_user,))

    # Create report
    r = client.post(
        "/time-bank/reports",
        headers={"Authorization": f"Bearer {reporter_token}"},
        json={"reported_member_id": mod_member, "reason": "no show"},
    )
    assert r.status_code == 200
    report_id = r.json()["report_id"]

    # ensure moderators notified
    with db_session() as conn:
        c = conn.execute(
            "SELECT COUNT(*) AS c FROM notifications WHERE member_id = ? AND event_type = 'report_created'",
            (mod_member,),
        ).fetchone()["c"]
        assert c == 1

    # moderator resolves
    r = client.post(
        f"/time-bank/reports/{report_id}/resolve",
        headers={"Authorization": f"Bearer {mod_token}"},
        json={"resolution_action": "warning"},
    )
    assert r.status_code == 200

    with db_session() as conn:
        row = conn.execute("SELECT status, resolution_action FROM reports WHERE id = ?", (report_id,)).fetchone()
        assert row["status"] == "resolved"
        assert row["resolution_action"] == "warning"
