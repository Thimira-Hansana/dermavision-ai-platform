from __future__ import annotations

from dataclasses import dataclass

from backend.main import app
from fastapi.testclient import TestClient


@dataclass
class DummyResult:
    predicted_class: str = "nv"
    diagnosis_name: str = "Melanocytic nevi"
    confidence: float = 0.91
    top_3_predictions: list[dict[str, float | str]] = None  # type: ignore[assignment]
    gradcam_path: str | None = "outputs/gradcam/mock.png"
    inference_time_ms: float = 12.0
    model_version: str = "test-model"
    timestamp: str = "2026-07-02T00:00:00+00:00"
    disclaimer: str = "demo disclaimer"
    model_ready: bool = True

    def __post_init__(self) -> None:
        if self.top_3_predictions is None:
            self.top_3_predictions = [
                {"class": "nv", "confidence": 0.91},
                {"class": "bkl", "confidence": 0.05},
                {"class": "mel", "confidence": 0.04},
            ]


class DummyInferenceService:
    def predict(self, _payload: bytes) -> DummyResult:
        return DummyResult()

    def info(self) -> dict[str, object]:
        return {
            "model_version": "test-model",
            "model_ready": True,
            "model_name": "efficientnet_b0",
            "class_labels": {"nv": "Melanocytic nevi"},
            "device": "cpu",
        }


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint(sample_image_bytes: bytes, monkeypatch) -> None:
    from backend.api.routes import predict as predict_route
    from backend.api.routes import system as system_route

    monkeypatch.setattr(predict_route, "get_inference_service", lambda: DummyInferenceService())
    monkeypatch.setattr(system_route, "get_inference_service", lambda: DummyInferenceService())
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            files={"file": ("sample.jpg", sample_image_bytes, "image/jpeg")},
        )
    assert response.status_code == 200
    assert response.json()["predicted_class"] == "nv"
