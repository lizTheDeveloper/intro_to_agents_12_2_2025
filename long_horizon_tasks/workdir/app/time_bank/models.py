from __future__ import annotations

from pydantic import BaseModel, Field


class MemberProfile(BaseModel):
    member_id: str
    user_id: str
    name: str
    contact: str
    area: str


class UpdateMemberProfileRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    contact: str | None = Field(default=None, min_length=1)
    area: str | None = Field(default=None, min_length=1)


class CreateOfferRequest(BaseModel):
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    estimated_hours: float = Field(gt=0)
    availability: str = Field(min_length=1)


class OfferResponse(BaseModel):
    offer_id: str


class CreateRequestRequest(BaseModel):
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    estimated_hours: float = Field(gt=0)
    preferred_time: str = Field(min_length=1)


class RequestResponse(BaseModel):
    request_id: str


class CreateHelpSessionRequest(BaseModel):
    helper_member_id: str
    recipient_member_id: str
    request_id: str | None = None
    offer_id: str | None = None


class HelpSessionResponse(BaseModel):
    session_id: str


class CompleteHelpSessionRequest(BaseModel):
    agreed_hours: float = Field(gt=0)
    funding_source: str = Field(pattern="^(member|community_bank|volunteer)$")


class BalanceResponse(BaseModel):
    owner_type: str
    owner_id: str
    hours: float


class LedgerEntry(BaseModel):
    id: str
    helper_member_id: str
    recipient_member_id: str | None
    hours: float
    funding_source: str
    created_at: str
    session_id: str


class CreateReportRequest(BaseModel):
    reported_member_id: str | None = None
    session_id: str | None = None
    reason: str = Field(min_length=1)


class ReportResponse(BaseModel):
    report_id: str


class ResolveReportRequest(BaseModel):
    resolution_action: str = Field(min_length=1)
