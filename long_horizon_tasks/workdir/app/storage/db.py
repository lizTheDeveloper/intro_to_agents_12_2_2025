import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbConfig:
    path: Path


def _default_db_path() -> Path:
    # Allow tests (and deployments) to override via env var.
    env = os.environ.get("TIMEBANK_DB_PATH")
    if env:
        return Path(env)
    return Path("./timebank.sqlite3")


DEFAULT_DB_CONFIG = DbConfig(path=_default_db_path())


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
          id TEXT PRIMARY KEY,
          email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL,
          created_at TEXT NOT NULL
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_roles (
          user_id TEXT PRIMARY KEY,
          role TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
          token TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          created_at TEXT NOT NULL,
          revoked_at TEXT,
          FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
          token TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          expires_at TEXT NOT NULL,
          used_at TEXT,
          created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
          id TEXT PRIMARY KEY,
          user_id TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          contact TEXT NOT NULL,
          area TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS offers (
          id TEXT PRIMARY KEY,
          member_id TEXT NOT NULL,
          category TEXT NOT NULL,
          description TEXT NOT NULL,
          estimated_hours REAL NOT NULL,
          availability TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(member_id) REFERENCES members(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
          id TEXT PRIMARY KEY,
          member_id TEXT NOT NULL,
          category TEXT NOT NULL,
          description TEXT NOT NULL,
          estimated_hours REAL NOT NULL,
          preferred_time TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(member_id) REFERENCES members(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS help_sessions (
          id TEXT PRIMARY KEY,
          helper_member_id TEXT NOT NULL,
          recipient_member_id TEXT NOT NULL,
          request_id TEXT,
          offer_id TEXT,
          status TEXT NOT NULL,
          agreed_hours REAL,
          funding_source TEXT,
          created_at TEXT NOT NULL,
          completed_at TEXT,
          FOREIGN KEY(helper_member_id) REFERENCES members(id),
          FOREIGN KEY(recipient_member_id) REFERENCES members(id),
          FOREIGN KEY(request_id) REFERENCES requests(id),
          FOREIGN KEY(offer_id) REFERENCES offers(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ledger_transactions (
          id TEXT PRIMARY KEY,
          helper_member_id TEXT NOT NULL,
          recipient_member_id TEXT,
          hours REAL NOT NULL,
          funding_source TEXT NOT NULL,
          created_at TEXT NOT NULL,
          session_id TEXT NOT NULL,
          FOREIGN KEY(helper_member_id) REFERENCES members(id),
          FOREIGN KEY(recipient_member_id) REFERENCES members(id),
          FOREIGN KEY(session_id) REFERENCES help_sessions(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS balances (
          owner_type TEXT NOT NULL,
          owner_id TEXT NOT NULL,
          hours REAL NOT NULL,
          updated_at TEXT NOT NULL,
          PRIMARY KEY(owner_type, owner_id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
          id TEXT PRIMARY KEY,
          reporter_member_id TEXT NOT NULL,
          reported_member_id TEXT,
          session_id TEXT,
          reason TEXT NOT NULL,
          status TEXT NOT NULL,
          resolution_action TEXT,
          created_at TEXT NOT NULL,
          resolved_at TEXT,
          FOREIGN KEY(reporter_member_id) REFERENCES members(id),
          FOREIGN KEY(reported_member_id) REFERENCES members(id),
          FOREIGN KEY(session_id) REFERENCES help_sessions(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notification_prefs (
          member_id TEXT PRIMARY KEY,
          on_new_request INTEGER NOT NULL,
          on_offer_accepted INTEGER NOT NULL,
          on_session_completed INTEGER NOT NULL,
          channel_email INTEGER NOT NULL,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(member_id) REFERENCES members(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
          id TEXT PRIMARY KEY,
          member_id TEXT NOT NULL,
          event_type TEXT NOT NULL,
          payload_json TEXT NOT NULL,
          status TEXT NOT NULL,
          failure_reason TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(member_id) REFERENCES members(id)
        )
        """
    )

    conn.commit()


def connect(config: DbConfig | None = None) -> sqlite3.Connection:
    if config is None:
        config = DbConfig(path=_default_db_path())
    conn = sqlite3.connect(str(config.path))
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return conn


@contextmanager
def db_session(config: DbConfig | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(config)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
