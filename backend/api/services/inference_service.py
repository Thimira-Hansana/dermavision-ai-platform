"""API-facing inference helpers."""

from __future__ import annotations

from functools import lru_cache

from dermavision_ai.inference.service import InferenceService


@lru_cache(maxsize=1)
def get_inference_service() -> InferenceService:
    return InferenceService()
