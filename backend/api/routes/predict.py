"""Prediction routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.session import get_db_session
from backend.api.repositories.history_repository import HistoryRepository
from backend.api.schemas import BatchPredictionResponse, PredictionItem, PredictionResponse
from backend.api.services.inference_service import get_inference_service
from backend.api.services.metrics import prediction_counter, prediction_latency
from backend.api.services.uploads import validate_upload
from dermavision_ai.inference.service import InferenceResult

router = APIRouter(prefix="/predict", tags=["prediction"])


def _build_response(result: InferenceResult) -> PredictionResponse:
    typed = result
    return PredictionResponse(
        predicted_class=typed.predicted_class,
        diagnosis_name=typed.diagnosis_name,
        confidence=typed.confidence,
        top_3_predictions=[PredictionItem(**item) for item in typed.top_3_predictions],
        gradcam_url=f"/{typed.gradcam_path}" if typed.gradcam_path else None,
        inference_time_ms=typed.inference_time_ms,
        model_version=typed.model_version,
        timestamp=typed.timestamp,
        disclaimer=typed.disclaimer,
        model_ready=typed.model_ready,
    )


@router.post("", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
) -> PredictionResponse:
    payload = await validate_upload(file)
    result = get_inference_service().predict(payload)
    response = _build_response(result)
    await HistoryRepository(session).create(
        filename=file.filename or "unknown",
        predicted_class=response.predicted_class,
        confidence=response.confidence,
        model_version=response.model_version,
        gradcam_url=response.gradcam_url,
        disclaimer=response.disclaimer,
    )
    prediction_counter.inc()
    prediction_latency.observe(response.inference_time_ms)
    return response


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    files: list[UploadFile] = File(...),
    session: AsyncSession = Depends(get_db_session),
) -> BatchPredictionResponse:
    predictions: list[PredictionResponse] = []
    repository = HistoryRepository(session)
    for file in files:
        payload = await validate_upload(file)
        result = get_inference_service().predict(payload)
        response = _build_response(result)
        await repository.create(
            filename=file.filename or "unknown",
            predicted_class=response.predicted_class,
            confidence=response.confidence,
            model_version=response.model_version,
            gradcam_url=response.gradcam_url,
            disclaimer=response.disclaimer,
        )
        prediction_counter.inc()
        prediction_latency.observe(response.inference_time_ms)
        predictions.append(response)
    return BatchPredictionResponse(predictions=predictions)
