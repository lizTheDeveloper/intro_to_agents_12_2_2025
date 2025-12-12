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
            "area": "any",
        },
    )
    r = client.post("/auth/login", json={"email": email, "password": "supersecret"})
    return r.json()["token"]


def test_authenticated_request_with_permissions_is_allowed():
    client = TestClient(app)
    token = _signup_and_login(client, "m1@example.com")

    r = client.get("/gateway/protected", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["role"] == "member"


def test_unauthenticated_request_is_rejected():
    client = TestClient(app)
    r = client.get("/gateway/protected")
    assert r.status_code == 401


def test_rate_limiter_exceeds_limit_returns_429():
    # rate limit applies to signup/login as "public" endpoints in this demo
    client = TestClient(app)

    # exceed limiter (5 req/sec) by making 6 signups quickly
    statuses = []
    for i in range(6):
        r = client.post(
            "/auth/signup",
            json={
                "name": "User",
                "email": f"rl{i}@example.com",
                "password": "supersecret",
                "contact": f"rl{i}@example.com",
                "area": "any",
            },
        )
        statuses.append(r.status_code)

    assert 429 in statuses
