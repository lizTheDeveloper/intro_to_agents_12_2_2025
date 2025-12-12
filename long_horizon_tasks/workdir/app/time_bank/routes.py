from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.gateway.authz import Principal, get_principal, require_role
from app.storage.db import db_session
from app.time_bank.models import (
    BalanceResponse,
    CompleteHelpSessionRequest,
    CreateHelpSessionRequest,
    CreateOfferRequest,
    CreateReportRequest,
    CreateRequestRequest,
    HelpSessionResponse,
    LedgerEntry,
    MemberProfile,
    OfferResponse,
    ReportResponse,
    RequestResponse,
    ResolveReportRequest,
    UpdateMemberProfileRequest,
)
from app.time_bank.service import (
    complete_help_session,
    create_help_session,
    create_offer,
    create_report,
    create_request,
    get_member_by_user,
    list_member_ledger,
    resolve_report,
    update_member,
)

router = APIRouter(prefix="/time-bank", tags=["time-bank"])


@router.get("/me", response_model=MemberProfile)
def get_my_profile(principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        row = get_member_by_user(conn, user_id=principal.user_id)
        if not row:
            raise HTTPException(status_code=404, detail="member_not_found")
        return MemberProfile(
            member_id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            contact=row["contact"],
            area=row["area"],
        )


@router.patch("/me", response_model=MemberProfile)
def update_my_profile(payload: UpdateMemberProfileRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        row = get_member_by_user(conn, user_id=principal.user_id)
        if not row:
            raise HTTPException(status_code=404, detail="member_not_found")
        update_member(conn, member_id=row["id"], name=payload.name, contact=payload.contact, area=payload.area)
        row2 = get_member_by_user(conn, user_id=principal.user_id)
        return MemberProfile(
            member_id=row2["id"],
            user_id=row2["user_id"],
            name=row2["name"],
            contact=row2["contact"],
            area=row2["area"],
        )


@router.post("/offers", response_model=OfferResponse)
def post_offer(payload: CreateOfferRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        member = get_member_by_user(conn, user_id=principal.user_id)
        if not member:
            raise HTTPException(status_code=404, detail="member_not_found")
        offer_id = create_offer(
            conn,
            member_id=member["id"],
            category=payload.category,
            description=payload.description,
            estimated_hours=payload.estimated_hours,
            availability=payload.availability,
        )
        return OfferResponse(offer_id=offer_id)


@router.post("/requests", response_model=RequestResponse)
def post_request(payload: CreateRequestRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        member = get_member_by_user(conn, user_id=principal.user_id)
        if not member:
            raise HTTPException(status_code=404, detail="member_not_found")
        request_id = create_request(
            conn,
            member_id=member["id"],
            category=payload.category,
            description=payload.description,
            estimated_hours=payload.estimated_hours,
            preferred_time=payload.preferred_time,
        )
        return RequestResponse(request_id=request_id)


@router.post("/help-sessions", response_model=HelpSessionResponse)
def create_session(payload: CreateHelpSessionRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        session_id = create_help_session(
            conn,
            helper_member_id=payload.helper_member_id,
            recipient_member_id=payload.recipient_member_id,
            request_id=payload.request_id,
            offer_id=payload.offer_id,
        )
        return HelpSessionResponse(session_id=session_id)


@router.post("/help-sessions/{session_id}/complete")
def complete_session(session_id: str, payload: CompleteHelpSessionRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        try:
            complete_help_session(
                conn,
                session_id=session_id,
                agreed_hours=payload.agreed_hours,
                funding_source=payload.funding_source,
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
    return {"status": "completed"}


@router.get("/balances/{owner_type}/{owner_id}", response_model=BalanceResponse)
def get_balance(owner_type: str, owner_id: str, principal: Principal = Depends(get_principal)):
    from app.time_bank.service import _get_balance

    with db_session() as conn:
        hours = _get_balance(conn, owner_type=owner_type, owner_id=owner_id)
        return BalanceResponse(owner_type=owner_type, owner_id=owner_id, hours=hours)


@router.get("/ledger/{member_id}", response_model=list[LedgerEntry])
def get_ledger(member_id: str, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        rows = list_member_ledger(conn, member_id=member_id)
        return [
            LedgerEntry(
                id=r["id"],
                helper_member_id=r["helper_member_id"],
                recipient_member_id=r["recipient_member_id"],
                hours=float(r["hours"]),
                funding_source=r["funding_source"],
                created_at=r["created_at"],
                session_id=r["session_id"],
            )
            for r in rows
        ]


@router.post("/reports", response_model=ReportResponse)
def report(payload: CreateReportRequest, principal: Principal = Depends(get_principal)):
    with db_session() as conn:
        reporter = get_member_by_user(conn, user_id=principal.user_id)
        if not reporter:
            raise HTTPException(status_code=404, detail="member_not_found")
        report_id = create_report(
            conn,
            reporter_member_id=reporter["id"],
            reported_member_id=payload.reported_member_id,
            session_id=payload.session_id,
            reason=payload.reason,
        )
        return ReportResponse(report_id=report_id)


@router.post("/reports/{report_id}/resolve")
def resolve(report_id: str, payload: ResolveReportRequest, principal: Principal = Depends(require_role("moderator", "admin"))):
    with db_session() as conn:
        try:
            resolve_report(conn, report_id=report_id, resolution_action=payload.resolution_action)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
    return {"status": "resolved"}
