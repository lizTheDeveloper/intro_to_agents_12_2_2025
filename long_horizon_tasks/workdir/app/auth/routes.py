from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request

from app.auth.models import (
    LoginRequest,
    LoginResponse,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    SignupRequest,
    SignupResponse,
)
from app.auth.service import (
    create_user_and_member,
    issue_password_reset_token,
    login,
    logout,
)
from app.gateway.rate_limit import public_rate_limit
from app.storage.db import db_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignupResponse)
def signup(payload: SignupRequest, request: Request):
    public_rate_limit(request)
    with db_session() as conn:
        try:
            user_id, member_id = create_user_and_member(
                conn,
                name=payload.name,
                email=str(payload.email),
                password=payload.password,
                contact=payload.contact,
                area=payload.area,
            )
        except Exception as e:
            # simplistic duplicate handling
            raise HTTPException(status_code=400, detail="signup_failed") from e
        return SignupResponse(user_id=user_id, member_id=member_id)


@router.post("/login", response_model=LoginResponse)
def login_route(payload: LoginRequest, request: Request):
    public_rate_limit(request)
    with db_session() as conn:
        token = login(conn, email=str(payload.email), password=payload.password)
        if not token:
            raise HTTPException(status_code=401, detail="invalid_credentials")
        return LoginResponse(token=token)


@router.post("/logout")
def logout_route(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing_token")
    token = authorization.split(" ", 1)[1].strip()
    with db_session() as conn:
        logout(conn, token=token)
    return {"status": "logged_out"}


@router.post("/password-reset", response_model=PasswordResetResponse)
def password_reset(payload: PasswordResetRequest, request: Request):
    public_rate_limit(request)
    with db_session() as conn:
        result = issue_password_reset_token(conn, email=str(payload.email))
        if not result:
            # Do not leak whether email exists
            raise HTTPException(status_code=200, detail="ok")
        token, expires_at = result
        return PasswordResetResponse(reset_token=token, expires_at=expires_at)


@router.post("/password-reset/confirm")
def password_reset_confirm(payload: PasswordResetConfirmRequest, request: Request):
    public_rate_limit(request)
    from app.auth.service import reset_password

    with db_session() as conn:
        ok = reset_password(conn, reset_token=payload.reset_token, new_password=payload.new_password)
        if not ok:
            raise HTTPException(status_code=400, detail="invalid_or_expired_token")
        return {"status": "password_updated"}
