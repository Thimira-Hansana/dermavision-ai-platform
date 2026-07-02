"""Model loading and inference service."""

from __future__ import annotations

import io
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image

from dermavision_ai.core.constants import CLASS_LABELS, CLASS_ORDER, ROOT_DIR
from dermavision_ai.core.settings import get_settings
from dermavision_ai.core.utils import ensure_directory, get_device
from dermavision_ai.explainability.gradcam import GradCAM, save_gradcam_artifacts
from dermavision_ai.models.model_factory import build_model, load_checkpoint
from dermavision_ai.training.metrics import top_k_predictions


@dataclass(slots=True)
class InferenceResult:
    predicted_class: str
    diagnosis_name: str
    confidence: float
    top_3_predictions: list[dict[str, float | str]]
    gradcam_path: str | None
    inference_time_ms: float
    model_version: str
    timestamp: str
    disclaimer: str
    model_ready: bool


class InferenceService:
    """Inference wrapper around the trained model artifact."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.device = get_device()
        self.image_size = int(self.settings.load_yaml_config().get("dataset", {}).get("image_size", 224))
        self.outputs_dir = ensure_directory(ROOT_DIR / "outputs" / "gradcam")
        self.disclaimer = str(
            self.settings.load_yaml_config().get("inference", {}).get(
                "disclaimer",
                "This application is for educational and research purposes only.",
            )
        )
        self.model, self.model_ready, self.model_version, self.loaded_model_name = self._load_model()
        self.gradcam = GradCAM(self.model)

    def _select_checkpoint(self) -> Path | None:
        configured = self.settings.model_checkpoint
        if configured:
            path = Path(configured)
            return path if path.exists() else None
        candidates = sorted(self.settings.model_dir.glob("*.pt"))
        return candidates[-1] if candidates else None

    def _load_model(self) -> tuple[torch.nn.Module, bool, str, str]:
        checkpoint = self._select_checkpoint()
        model_name = self.settings.default_model
        version = "untrained-demo"
        ready = False
        if checkpoint is not None:
            payload = torch.load(checkpoint, map_location=str(self.device))
            model_name = str(payload.get("model_name", model_name))
            model = build_model(model_name, num_classes=len(CLASS_ORDER), pretrained=False).to(self.device)
            load_checkpoint(model, checkpoint, map_location=str(self.device))
            version = checkpoint.stem
            ready = True
        else:
            model = build_model(model_name, num_classes=len(CLASS_ORDER), pretrained=False).to(self.device)
        model.eval()
        return model, ready, version, model_name

    def _prepare_tensor(self, image_bytes: bytes) -> tuple[torch.Tensor, np.ndarray]:
        with Image.open(io.BytesIO(image_bytes)) as image:
            rgb = image.convert("RGB").resize((self.image_size, self.image_size))
        array = np.array(rgb)
        tensor = torch.tensor(array / 255.0, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
        mean = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32).view(1, 3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32).view(1, 3, 1, 1)
        normalized = (tensor - mean) / std
        return normalized.to(self.device), array

    def predict(self, image_bytes: bytes) -> InferenceResult:
        started = time.perf_counter()
        inputs, rgb_image = self._prepare_tensor(image_bytes)
        with torch.no_grad():
            logits = self.model(inputs)
            probabilities = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
        predicted_index = int(probabilities.argmax())
        predicted_class = CLASS_ORDER[predicted_index]
        cam = self.gradcam.generate(inputs, class_index=predicted_index)
        output_path = self.outputs_dir / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}.png"
        save_gradcam_artifacts(rgb_image, cam, output_path)
        elapsed_ms = (time.perf_counter() - started) * 1000
        return InferenceResult(
            predicted_class=predicted_class,
            diagnosis_name=CLASS_LABELS[predicted_class],
            confidence=float(probabilities[predicted_index]),
            top_3_predictions=top_k_predictions(probabilities, CLASS_ORDER, top_k=3),
            gradcam_path=str(output_path.relative_to(ROOT_DIR)),
            inference_time_ms=elapsed_ms,
            model_version=self.model_version,
            timestamp=datetime.now(UTC).isoformat(),
            disclaimer=self.disclaimer,
            model_ready=self.model_ready,
        )

    def info(self) -> dict[str, Any]:
        return {
            "model_version": self.model_version,
            "model_ready": self.model_ready,
            "model_name": self.loaded_model_name,
            "class_labels": CLASS_LABELS,
            "device": str(self.device),
        }
