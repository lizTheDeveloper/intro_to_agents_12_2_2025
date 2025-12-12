from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.gateway.authz import Principal, get_principal
from app.notifications.models import DeliveryAttemptRequest, NotificationPrefs, UpdateNotificationPrefsRequest
from app.notifications.service import get_prefs, record_delivery_attempt, update_prefs
from app.storage.db import db_session
from app.time_bank.service import get_member_by_user

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/prefs", response_model=NotificationPrefs)
def get_my_prefs(principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        member = get_member_by_user(conn, user_id=principal.user_id)
        if not member:
            raise HTTPException(status_code=404, detail="member_not_found")
        row = get_prefs(conn, member_id=member["id"])
        if not row:
            raise HTTPException(status_code=404, detail="prefs_not_found")
        return NotificationPrefs(
            on_new_request=bool(row["on_new_request"]),
            on_offer_accepted=bool(row["on_offer_accepted"]),
            on_session_completed=bool(row["on_session_completed"]),
            channel_email=bool(row["channel_email"]),
        )


@router.patch("/prefs", response_model=NotificationPrefs)
def update_my_prefs(payload: UpdateNotificationPrefsRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        member = get_member_by_user(conn, user_id=principal.user_id)
        if not member:
            raise HTTPException(status_code=404, detail="member_not_found")
        try:
            update_prefs(
                conn,
                member_id=member["id"],
                on_new_request=payload.on_new_request,
                on_offer_accepted=payload.on_offer_accepted,
                on_session_completed=payload.on_session_completed,
                channel_email=payload.channel_email,
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        row = get_prefs(conn, member_id=member["id"])
        return NotificationPrefs(
            on_new_request=bool(row["on_new_request"]),
            on_offer_accepted=bool(row["on_offer_accepted"]),
            on_session_completed=bool(row["on_session_completed"]),
            channel_email=bool(row["channel_email"]),
        )


@router.post("/deliver")
def deliver_notification(payload: DeliveryAttemptRequest, principal: Principal = Depends(get_principal)):
    # For now, any authenticated user can report delivery (stub for an email worker)
    with db_session() as conn:
        try:
            record_delivery_attempt(
                conn,
                notification_id=payload.notification_id,
                status=payload.status,
                failure_reason=payload.failure_reason,
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
    return {"status": "recorded"}
