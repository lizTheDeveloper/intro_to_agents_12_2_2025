from __future__ import annotations

from fastapi import APIRouter, Depends

from app.gateway.authz import Principal, require_role

router = APIRouter(prefix="/gateway", tags=["gateway"])


@router.get("/protected")
def protected_endpoint(principal: Principal = Depends(require_role("member", "admin", "moderator"))):
    return {"user_id": principal.user_id, "role": principal.role}
