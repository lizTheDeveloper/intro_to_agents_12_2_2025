from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_member_by_user(conn: sqlite3.Connection, *, user_id: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM members WHERE user_id = ?", (user_id,)).fetchone()


def update_member(conn: sqlite3.Connection, *, member_id: str, name: str | None, contact: str | None, area: str | None) -> None:
    row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    if not row:
        raise ValueError("member_not_found")
    new_name = name if name is not None else row["name"]
    new_contact = contact if contact is not None else row["contact"]
    new_area = area if area is not None else row["area"]
    conn.execute(
        "UPDATE members SET name = ?, contact = ?, area = ? WHERE id = ?",
        (new_name, new_contact, new_area, member_id),
    )


def create_offer(
    conn: sqlite3.Connection,
    *,
    member_id: str,
    category: str,
    description: str,
    estimated_hours: float,
    availability: str,
) -> str:
    offer_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO offers (id, member_id, category, description, estimated_hours, availability, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (offer_id, member_id, category, description, estimated_hours, availability, utcnow()),
    )
    return offer_id


def create_request(
    conn: sqlite3.Connection,
    *,
    member_id: str,
    category: str,
    description: str,
    estimated_hours: float,
    preferred_time: str,
) -> str:
    request_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO requests (id, member_id, category, description, estimated_hours, preferred_time, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (request_id, member_id, category, description, estimated_hours, preferred_time, utcnow()),
    )

    _enqueue_notifications_for_new_request(conn, request_id=request_id, category=category)

    return request_id


def _enqueue_notifications_for_new_request(conn: sqlite3.Connection, *, request_id: str, category: str) -> None:
    rows = conn.execute(
        """
        SELECT np.member_id
        FROM notification_prefs np
        WHERE np.on_new_request = 1 AND np.channel_email = 1
        """
    ).fetchall()

    payload = {"request_id": request_id, "category": category}
    for r in rows:
        nid = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO notifications (id, member_id, event_type, payload_json, status, failure_reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
            (nid, r["member_id"], "new_help_request", json.dumps(payload), "pending", utcnow(), utcnow()),
        )


def _get_balance(conn: sqlite3.Connection, *, owner_type: str, owner_id: str) -> float:
    row = conn.execute(
        "SELECT hours FROM balances WHERE owner_type = ? AND owner_id = ?",
        (owner_type, owner_id),
    ).fetchone()
    return float(row["hours"]) if row else 0.0


def _set_balance(conn: sqlite3.Connection, *, owner_type: str, owner_id: str, hours: float) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO balances (owner_type, owner_id, hours, updated_at) VALUES (?, ?, ?, ?)",
        (owner_type, owner_id, float(hours), utcnow()),
    )


def create_help_session(
    conn: sqlite3.Connection,
    *,
    helper_member_id: str,
    recipient_member_id: str,
    request_id: str | None,
    offer_id: str | None,
) -> str:
    session_id = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO help_sessions (id, helper_member_id, recipient_member_id, request_id, offer_id, status, agreed_hours, funding_source, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, NULL)
        """,
        (session_id, helper_member_id, recipient_member_id, request_id, offer_id, "scheduled", utcnow()),
    )

    _enqueue_offer_accepted_notifications(conn, helper_member_id=helper_member_id, recipient_member_id=recipient_member_id, session_id=session_id)
    return session_id


def _enqueue_offer_accepted_notifications(conn: sqlite3.Connection, *, helper_member_id: str, recipient_member_id: str, session_id: str) -> None:
    payload = {"session_id": session_id}
    for member_id in (helper_member_id, recipient_member_id):
        pref = conn.execute(
            "SELECT on_offer_accepted, channel_email FROM notification_prefs WHERE member_id = ?",
            (member_id,),
        ).fetchone()
        if pref and int(pref["on_offer_accepted"]) == 1 and int(pref["channel_email"]) == 1:
            nid = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO notifications (id, member_id, event_type, payload_json, status, failure_reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
                (nid, member_id, "offer_accepted", json.dumps(payload), "pending", utcnow(), utcnow()),
            )


def complete_help_session(
    conn: sqlite3.Connection,
    *,
    session_id: str,
    agreed_hours: float,
    funding_source: str,
) -> None:
    session = conn.execute("SELECT * FROM help_sessions WHERE id = ?", (session_id,)).fetchone()
    if not session:
        raise ValueError("session_not_found")

    helper_id = session["helper_member_id"]
    recipient_id = session["recipient_member_id"]

    # volunteer sessions credit community bank pool
    if funding_source == "volunteer":
        bank_balance = _get_balance(conn, owner_type="community_bank", owner_id="pool")
        _set_balance(conn, owner_type="community_bank", owner_id="pool", hours=bank_balance + agreed_hours)
        # optional personal bonus not implemented (spec says MAY)
        recipient_id_for_ledger = None
    else:
        # Update helper balance
        helper_balance = _get_balance(conn, owner_type="member", owner_id=helper_id)
        _set_balance(conn, owner_type="member", owner_id=helper_id, hours=helper_balance + agreed_hours)

        if funding_source == "member":
            recipient_balance = _get_balance(conn, owner_type="member", owner_id=recipient_id)
            _set_balance(conn, owner_type="member", owner_id=recipient_id, hours=recipient_balance - agreed_hours)
        else:
            bank_balance = _get_balance(conn, owner_type="community_bank", owner_id="pool")
            _set_balance(conn, owner_type="community_bank", owner_id="pool", hours=bank_balance - agreed_hours)

        recipient_id_for_ledger = recipient_id

    # Ledger entry
    ledger_id = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO ledger_transactions (id, helper_member_id, recipient_member_id, hours, funding_source, created_at, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (ledger_id, helper_id, recipient_id_for_ledger, float(agreed_hours), funding_source, utcnow(), session_id),
    )

    conn.execute(
        "UPDATE help_sessions SET status = ?, agreed_hours = ?, funding_source = ?, completed_at = ? WHERE id = ?",
        ("completed", float(agreed_hours), funding_source, utcnow(), session_id),
    )

    if funding_source != "volunteer":
        _enqueue_session_completed_notifications(
            conn,
            helper_member_id=helper_id,
            recipient_member_id=recipient_id,
            session_id=session_id,
            agreed_hours=agreed_hours,
            funding_source=funding_source,
        )


def _enqueue_session_completed_notifications(
    conn: sqlite3.Connection,
    *,
    helper_member_id: str,
    recipient_member_id: str,
    session_id: str,
    agreed_hours: float,
    funding_source: str,
) -> None:
    payload = {"session_id": session_id, "agreed_hours": agreed_hours, "funding_source": funding_source}
    for member_id in (helper_member_id, recipient_member_id):
        pref = conn.execute(
            "SELECT on_session_completed, channel_email FROM notification_prefs WHERE member_id = ?",
            (member_id,),
        ).fetchone()
        if pref and int(pref["on_session_completed"]) == 1 and int(pref["channel_email"]) == 1:
            nid = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO notifications (id, member_id, event_type, payload_json, status, failure_reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
                (nid, member_id, "session_completed", json.dumps(payload), "pending", utcnow(), utcnow()),
            )


def list_member_ledger(conn: sqlite3.Connection, *, member_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT * FROM ledger_transactions
        WHERE helper_member_id = ? OR recipient_member_id = ?
        ORDER BY created_at DESC
        """,
        (member_id, member_id),
    ).fetchall()


def create_report(
    conn: sqlite3.Connection,
    *,
    reporter_member_id: str,
    reported_member_id: str | None,
    session_id: str | None,
    reason: str,
) -> str:
    report_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO reports (id, reporter_member_id, reported_member_id, session_id, reason, status, resolution_action, created_at, resolved_at) VALUES (?, ?, ?, ?, ?, ?, NULL, ?, NULL)",
        (report_id, reporter_member_id, reported_member_id, session_id, reason, "open", utcnow()),
    )
    # notify moderators/admins: record notifications to those roles
    rows = conn.execute(
        """
        SELECT m.id AS member_id
        FROM members m
        JOIN user_roles ur ON ur.user_id = m.user_id
        WHERE ur.role IN ('moderator', 'admin')
        """
    ).fetchall()
    payload = {"report_id": report_id}
    for r in rows:
        nid = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO notifications (id, member_id, event_type, payload_json, status, failure_reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
            (nid, r["member_id"], "report_created", json.dumps(payload), "pending", utcnow(), utcnow()),
        )
    return report_id


def resolve_report(conn: sqlite3.Connection, *, report_id: str, resolution_action: str) -> None:
    row = conn.execute("SELECT id FROM reports WHERE id = ?", (report_id,)).fetchone()
    if not row:
        raise ValueError("report_not_found")
    conn.execute(
        "UPDATE reports SET status = ?, resolution_action = ?, resolved_at = ? WHERE id = ?",
        ("resolved", resolution_action, utcnow(), report_id),
    )
