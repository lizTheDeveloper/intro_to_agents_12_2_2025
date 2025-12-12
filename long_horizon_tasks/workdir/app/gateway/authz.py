from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException

from app.auth.service import get_user_id_for_token
from app.storage.db import db_session


@dataclass(frozen=True)
class Principal:
    user_id: str
    role: str


def get_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing_token")
    token = authorization.split(" ", 1)[1].strip()
    with db_session() as conn:
        user_id = get_user_id_for_token(conn, token=token)
        if not user_id:
            raise HTTPException(status_code=401, detail="invalid_token")
        row = conn.execute("SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchone()
        role = row["role"] if row else "member"
        return Principal(user_id=user_id, role=role)


def require_role(*roles: str):
    def _dep(principal: Principal = Depends(get_principal)) -> Principal:
        if principal.role not in roles:
            raise HTTPException(status_code=403, detail="forbidden")
        return principal

    return _dep
