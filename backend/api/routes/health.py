"""Health route."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter

from backend.api.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(UTC).isoformat())
