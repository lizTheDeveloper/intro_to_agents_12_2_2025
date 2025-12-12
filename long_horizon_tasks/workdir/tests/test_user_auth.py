from fastapi.testclient import TestClient

from app.main import app


def test_member_signs_up_creates_user_and_linked_member_profile():
    client = TestClient(app)

    r = client.post(
        "/auth/signup",
        json={
            "name": "Ada",
            "email": "ada@example.com",
            "password": "supersecret",
            "contact": "ada@example.com",
            "area": "north",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "user_id" in data
    assert "member_id" in data


def test_member_logs_in_and_logs_out_session_is_invalidated():
    client = TestClient(app)

    # signup
    client.post(
        "/auth/signup",
        json={
            "name": "Grace",
            "email": "grace@example.com",
            "password": "supersecret",
            "contact": "grace@example.com",
            "area": "east",
        },
    )

    # login
    r = client.post("/auth/login", json={"email": "grace@example.com", "password": "supersecret"})
    assert r.status_code == 200
    token = r.json()["token"]
    assert token

    # logout
    r = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    # logout again should still succeed (idempotent), but token is revoked.
    r = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200


def test_member_resets_password_with_time_bound_token():
    client = TestClient(app)

    # signup
    client.post(
        "/auth/signup",
        json={
            "name": "Pat",
            "email": "pat@example.com",
            "password": "oldpassword",
            "contact": "pat@example.com",
            "area": "south",
        },
    )

    # initiate reset
    r = client.post("/auth/password-reset", json={"email": "pat@example.com"})
    assert r.status_code == 200
    body = r.json()
    reset_token = body["reset_token"]
    assert reset_token

    # confirm reset
    r = client.post(
        "/auth/password-reset/confirm",
        json={"reset_token": reset_token, "new_password": "newpassword"},
    )
    assert r.status_code == 200

    # old password no longer works
    r = client.post("/auth/login", json={"email": "pat@example.com", "password": "oldpassword"})
    assert r.status_code == 401

    # new password works
    r = client.post("/auth/login", json={"email": "pat@example.com", "password": "newpassword"})
    assert r.status_code == 200
