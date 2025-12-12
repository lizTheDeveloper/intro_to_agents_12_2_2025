from __future__ import annotations

import time
from dataclasses import dataclass

from fastapi import HTTPException, Request


@dataclass
class RateLimiter:
    limit: int
    window_seconds: int

    def __post_init__(self):
        self._hits: dict[str, list[float]] = {}

    def check(self, key: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds
        hits = self._hits.get(key, [])
        hits = [t for t in hits if t >= window_start]
        if len(hits) >= self.limit:
            raise HTTPException(status_code=429, detail="rate_limit_exceeded")
        hits.append(now)
        self._hits[key] = hits


# Global (in-memory) limiter for demo/testing
PUBLIC_LIMITER = RateLimiter(limit=5, window_seconds=1)


def public_rate_limit(request: Request) -> None:
    # Use client host if available, else a fallback.
    host = request.client.host if request.client else "unknown"
    PUBLIC_LIMITER.check(host)
