from __future__ import annotations

from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.gateway.routes import router as gateway_router
from app.notifications.routes import router as notifications_router
from app.storage.db import db_session
from app.time_bank.routes import router as time_bank_router

app = FastAPI(title="Time Bank")
app.include_router(auth_router)
app.include_router(gateway_router)
app.include_router(time_bank_router)
app.include_router(notifications_router)


@app.get("/health")
def health():
    # Ensure DB is reachable (basic readiness)
    with db_session() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}
