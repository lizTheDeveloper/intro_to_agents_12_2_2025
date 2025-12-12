from __future__ import annotations

from pydantic import BaseModel, Field


class NotificationPrefs(BaseModel):
    on_new_request: bool
    on_offer_accepted: bool
    on_session_completed: bool
    channel_email: bool


class UpdateNotificationPrefsRequest(BaseModel):
    on_new_request: bool | None = None
    on_offer_accepted: bool | None = None
    on_session_completed: bool | None = None
    channel_email: bool | None = None


class DeliveryAttemptRequest(BaseModel):
    notification_id: str
    status: str = Field(pattern="^(sent|failed)$")
    failure_reason: str | None = None
