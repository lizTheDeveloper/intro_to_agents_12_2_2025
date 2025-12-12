from __future__ import annotations

import secrets
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.auth.security import hash_password, verify_password


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AuthResult:
    token: str


def create_user_and_member(
    conn: sqlite3.Connection,
    *,
    name: str,
    email: str,
    password: str,
    contact: str,
    area: str,
) -> tuple[str, str]:
    user_id = str(uuid.uuid4())
    member_id = str(uuid.uuid4())

    conn.execute(
        "INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (user_id, email.lower(), hash_password(password), utcnow()),
    )

    # default role: member
    conn.execute(
        "INSERT INTO user_roles (user_id, role, created_at) VALUES (?, ?, ?)",
        (user_id, "member", utcnow()),
    )

    conn.execute(
        "INSERT INTO members (id, user_id, name, contact, area, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (member_id, user_id, name, contact, area, utcnow()),
    )

    # initialize personal balance to 0
    conn.execute(
        "INSERT OR REPLACE INTO balances (owner_type, owner_id, hours, updated_at) VALUES (?, ?, ?, ?)",
        ("member", member_id, 0.0, utcnow()),
    )

    # initialize notification prefs defaults: all on, email on
    conn.execute(
        "INSERT OR REPLACE INTO notification_prefs (member_id, on_new_request, on_offer_accepted, on_session_completed, channel_email, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (member_id, 1, 1, 1, 1, utcnow(), utcnow()),
    )

    return user_id, member_id


def login(conn: sqlite3.Connection, *, email: str, password: str) -> str | None:
    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        (email.lower(),),
    ).fetchone()
    if not row:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions (token, user_id, created_at, revoked_at) VALUES (?, ?, ?, NULL)",
        (token, row["id"], utcnow()),
    )
    return token


def logout(conn: sqlite3.Connection, *, token: str) -> None:
    conn.execute(
        "UPDATE sessions SET revoked_at = ? WHERE token = ? AND revoked_at IS NULL",
        (utcnow(), token),
    )


def get_user_id_for_token(conn: sqlite3.Connection, *, token: str) -> str | None:
    row = conn.execute(
        "SELECT user_id FROM sessions WHERE token = ? AND revoked_at IS NULL",
        (token,),
    ).fetchone()
    return row["user_id"] if row else None


def issue_password_reset_token(conn: sqlite3.Connection, *, email: str, ttl_minutes: int = 30) -> tuple[str, str] | None:
    row = conn.execute("SELECT id FROM users WHERE email = ?", (email.lower(),)).fetchone()
    if not row:
        return None
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).isoformat()
    conn.execute(
        "INSERT INTO password_reset_tokens (token, user_id, expires_at, used_at, created_at) VALUES (?, ?, ?, NULL, ?)",
        (token, row["id"], expires_at, utcnow()),
    )
    return token, expires_at


def reset_password(conn: sqlite3.Connection, *, reset_token: str, new_password: str) -> bool:
    row = conn.execute(
        "SELECT user_id, expires_at, used_at FROM password_reset_tokens WHERE token = ?",
        (reset_token,),
    ).fetchone()
    if not row:
        return False
    if row["used_at"] is not None:
        return False

    expires = datetime.fromisoformat(row["expires_at"])
    if expires < datetime.now(timezone.utc):
        return False

    conn.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (hash_password(new_password), row["user_id"]),
    )
    conn.execute(
        "UPDATE password_reset_tokens SET used_at = ? WHERE token = ?",
        (utcnow(), reset_token),
    )
    return True
