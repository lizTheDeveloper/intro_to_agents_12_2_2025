from __future__ import annotations

import sqlite3
from datetime import datetime, timezone


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_prefs(conn: sqlite3.Connection, *, member_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM notification_prefs WHERE member_id = ?", (member_id,)).fetchone()


def update_prefs(
    conn: sqlite3.Connection,
    *,
    member_id: str,
    on_new_request: bool | None,
    on_offer_accepted: bool | None,
    on_session_completed: bool | None,
    channel_email: bool | None,
) -> None:
    row = get_prefs(conn, member_id=member_id)
    if not row:
        raise ValueError("prefs_not_found")

    def _val(col: str, new: bool | None) -> int:
        return int(new) if new is not None else int(row[col])

    conn.execute(
        """
        UPDATE notification_prefs
        SET on_new_request = ?, on_offer_accepted = ?, on_session_completed = ?, channel_email = ?, updated_at = ?
        WHERE member_id = ?
        """,
        (
            _val("on_new_request", on_new_request),
            _val("on_offer_accepted", on_offer_accepted),
            _val("on_session_completed", on_session_completed),
            _val("channel_email", channel_email),
            utcnow(),
            member_id,
        ),
    )


def record_delivery_attempt(
    conn: sqlite3.Connection,
    *,
    notification_id: str,
    status: str,
    failure_reason: str | None,
) -> None:
    # Minimal "avoid excessive retries": if it's already failed, don't keep flipping/rewriting.
    row = conn.execute("SELECT status FROM notifications WHERE id = ?", (notification_id,)).fetchone()
    if not row:
        raise ValueError("notification_not_found")

    existing = row["status"]
    if existing in ("failed", "sent"):
        return

    if status == "failed" and not failure_reason:
        failure_reason = "unknown"

    conn.execute(
        "UPDATE notifications SET status = ?, failure_reason = ?, updated_at = ? WHERE id = ?",
        (status, failure_reason, utcnow(), notification_id),
    )
