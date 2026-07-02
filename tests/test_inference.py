from __future__ import annotations

from dermavision_ai.inference.service import InferenceService


def test_inference_service_info_has_core_fields() -> None:
    service = InferenceService()
    info = service.info()
    assert "model_version" in info
    assert "class_labels" in info
