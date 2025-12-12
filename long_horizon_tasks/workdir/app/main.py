from __future__ import annotations

from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.gateway.routes import router as gateway_router
from app.storage.db import db_session

app = FastAPI(title="Time Bank")
app.include_router(auth_router)
app.include_router(gateway_router)


@app.get("/health")
def health():
    # Ensure DB is reachable (basic readiness)
    with db_session() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}
