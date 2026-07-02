"""API schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PredictionItem(BaseModel):
    class_name: str = Field(alias="class")
    confidence: float

    model_config = {"populate_by_name": True}


class PredictionResponse(BaseModel):
    predicted_class: str
    diagnosis_name: str
    confidence: float
    top_3_predictions: list[PredictionItem]
    gradcam_url: str | None
    inference_time_ms: float
    model_version: str
    timestamp: str
    disclaimer: str
    model_ready: bool


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class PredictionHistoryResponse(BaseModel):
    id: int
    filename: str
    predicted_class: str
    confidence: float
    model_version: str
    created_at: datetime
    gradcam_url: str | None


class VersionResponse(BaseModel):
    version: str
    environment: str


class ModelInfoResponse(BaseModel):
    model_version: str
    model_ready: bool
    model_name: str
    class_labels: dict[str, str]
    device: str
