from fastapi.testclient import TestClient

from app.main import app


def _signup_and_login(client: TestClient, email: str, *, name: str = "User") -> tuple[str, str]:
    # returns (token, member_id)
    r = client.post(
        "/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": "supersecret",
            "contact": email,
            "area": "zone1",
        },
    )
    member_id = r.json()["member_id"]
    r = client.post("/auth/login", json={"email": email, "password": "supersecret"})
    token = r.json()["token"]
    return token, member_id


def test_member_earns_hours_by_helping_another_member_and_ledger_records():
    client = TestClient(app)
    helper_token, helper_member = _signup_and_login(client, "helper@example.com")
    recip_token, recip_member = _signup_and_login(client, "recip@example.com")

    # create help session
    r = client.post(
        "/time-bank/help-sessions",
        headers={"Authorization": f"Bearer {helper_token}"},
        json={"helper_member_id": helper_member, "recipient_member_id": recip_member},
    )
    assert r.status_code == 200
    session_id = r.json()["session_id"]

    # complete session funded by member
    r = client.post(
        f"/time-bank/help-sessions/{session_id}/complete",
        headers={"Authorization": f"Bearer {helper_token}"},
        json={"agreed_hours": 1.5, "funding_source": "member"},
    )
    assert r.status_code == 200

    # check balances
    r = client.get(
        f"/time-bank/balances/member/{helper_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()["hours"] == 1.5

    r = client.get(
        f"/time-bank/balances/member/{recip_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()["hours"] == -1.5

    # ledger history visible
    r = client.get(
        f"/time-bank/ledger/{helper_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.status_code == 200
    assert len(r.json()) >= 1
    assert r.json()[0]["session_id"] == session_id


def test_member_redeems_hours_from_community_bank_records_funding_source():
    client = TestClient(app)
    helper_token, helper_member = _signup_and_login(client, "helper2@example.com")
    recip_token, recip_member = _signup_and_login(client, "recip2@example.com")

    # seed community bank pool with hours directly for now
    from app.storage.db import db_session
    from app.time_bank.service import _set_balance

    with db_session() as conn:
        _set_balance(conn, owner_type="community_bank", owner_id="pool", hours=10.0)

    r = client.post(
        "/time-bank/help-sessions",
        headers={"Authorization": f"Bearer {helper_token}"},
        json={"helper_member_id": helper_member, "recipient_member_id": recip_member},
    )
    session_id = r.json()["session_id"]

    r = client.post(
        f"/time-bank/help-sessions/{session_id}/complete",
        headers={"Authorization": f"Bearer {helper_token}"},
        json={"agreed_hours": 2.0, "funding_source": "community_bank"},
    )
    assert r.status_code == 200

    # helper increases, recipient not decreased
    r = client.get(
        f"/time-bank/balances/member/{helper_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()["hours"] == 2.0

    r = client.get(
        f"/time-bank/balances/member/{recip_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()["hours"] == 0.0

    r = client.get(
        "/time-bank/balances/community_bank/pool",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()["hours"] == 8.0

    # ledger funding source
    r = client.get(
        f"/time-bank/ledger/{helper_member}",
        headers={"Authorization": f"Bearer {helper_token}"},
    )
    assert r.json()[0]["funding_source"] == "community_bank"
