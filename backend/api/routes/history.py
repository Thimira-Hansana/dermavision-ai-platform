"""History routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.session import get_db_session
from backend.api.repositories.history_repository import HistoryRepository
from backend.api.schemas import PredictionHistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[PredictionHistoryResponse])
async def list_history(session: AsyncSession = Depends(get_db_session)) -> list[PredictionHistoryResponse]:
    records = await HistoryRepository(session).list_recent()
    return [
        PredictionHistoryResponse(
            id=record.id,
            filename=record.filename,
            predicted_class=record.predicted_class,
            confidence=record.confidence,
            model_version=record.model_version,
            created_at=record.created_at,
            gradcam_url=record.gradcam_url,
        )
        for record in records
    ]
