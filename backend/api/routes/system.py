"""System information routes."""

from __future__ import annotations

from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from backend.api.schemas import ModelInfoResponse, VersionResponse
from backend.api.services.inference_service import get_inference_service
from dermavision_ai import __version__
from dermavision_ai.core.settings import get_settings

router = APIRouter(tags=["system"])


@router.get("/version", response_model=VersionResponse)
async def version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(version=__version__, environment=settings.env)


@router.get("/model-info", response_model=ModelInfoResponse)
async def model_info() -> ModelInfoResponse:
    return ModelInfoResponse(**get_inference_service().info())


@router.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
