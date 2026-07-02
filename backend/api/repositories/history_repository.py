"""History persistence."""

from __future__ import annotations

from backend.api.db.models import PredictionHistory
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HistoryRepository:
    """Access prediction history storage."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        filename: str,
        predicted_class: str,
        confidence: float,
        model_version: str,
        gradcam_url: str | None,
        disclaimer: str,
    ) -> PredictionHistory:
        record = PredictionHistory(
            filename=filename,
            predicted_class=predicted_class,
            confidence=confidence,
            model_version=model_version,
            gradcam_url=gradcam_url,
            disclaimer=disclaimer,
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def list_recent(self, limit: int = 25) -> list[PredictionHistory]:
        query = select(PredictionHistory).order_by(PredictionHistory.created_at.desc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
