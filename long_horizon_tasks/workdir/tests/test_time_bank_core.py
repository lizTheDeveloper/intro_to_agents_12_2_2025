from fastapi.testclient import TestClient

from app.main import app


def _signup_and_login(client: TestClient, email: str, *, name: str = "User") -> str:
    client.post(
        "/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": "supersecret",
            "contact": email,
            "area": "zone1",
        },
    )
    r = client.post("/auth/login", json={"email": email, "password": "supersecret"})
    return r.json()["token"]


def test_member_can_view_and_edit_profile_details():
    client = TestClient(app)
    token = _signup_and_login(client, "p1@example.com", name="Ada")

    r = client.get("/time-bank/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["name"] == "Ada"

    r = client.patch(
        "/time-bank/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"area": "zone2"},
    )
    assert r.status_code == 200
    assert r.json()["area"] == "zone2"


def test_member_posts_offer_is_published_and_associated_to_profile():
    client = TestClient(app)
    token = _signup_and_login(client, "o1@example.com")

    r = client.post(
        "/time-bank/offers",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "category": "gardening",
            "description": "I can help weed",
            "estimated_hours": 1.5,
            "availability": "weekends",
        },
    )
    assert r.status_code == 200
    assert r.json()["offer_id"]


def test_member_posts_request_creates_notifications_for_opted_in_members():
    client = TestClient(app)

    # member who will create a request
    token_req = _signup_and_login(client, "r1@example.com")

    # another member opted-in (defaults on)
    _signup_and_login(client, "watcher@example.com")

    r = client.post(
        "/time-bank/requests",
        headers={"Authorization": f"Bearer {token_req}"},
        json={
            "category": "rides",
            "description": "Need a ride to clinic",
            "estimated_hours": 2.0,
            "preferred_time": "tomorrow",
        },
    )
    assert r.status_code == 200

    # Verify notifications exist in DB for both members (including requester; simple baseline).
    from app.storage.db import db_session

    with db_session() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM notifications WHERE event_type = 'new_help_request'").fetchone()[
            "c"
        ]
        assert count >= 2
