"""Grad-CAM implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch
from PIL import Image
from torch import nn


def _infer_target_layer(model: nn.Module) -> nn.Module:
    for module in reversed(list(model.modules())):
        if isinstance(module, nn.Conv2d):
            return module
    raise ValueError("No convolutional layer found for Grad-CAM.")


class GradCAM:
    """Generate Grad-CAM heatmaps for convolutional models."""

    def __init__(self, model: nn.Module, target_layer: nn.Module | None = None) -> None:
        self.model = model
        self.target_layer = target_layer or _infer_target_layer(model)
        self.activations: torch.Tensor | None = None
        self.gradients: torch.Tensor | None = None
        self._register_hooks()

    def _register_hooks(self) -> None:
        self.target_layer.register_forward_hook(self._save_activations)
        self.target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, _module: nn.Module, _inputs: Any, output: torch.Tensor) -> None:
        self.activations = output.detach()

    def _save_gradients(self, _module: nn.Module, _grad_input: Any, grad_output: Any) -> None:
        self.gradients = grad_output[0].detach()

    def generate(self, inputs: torch.Tensor, class_index: int | None = None) -> np.ndarray:
        self.model.zero_grad(set_to_none=True)
        logits = self.model(inputs)
        target = logits.argmax(dim=1).item() if class_index is None else class_index
        logits[:, target].sum().backward()
        if self.activations is None or self.gradients is None:
            raise RuntimeError("Grad-CAM hooks did not capture activations.")
        pooled_grads = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (pooled_grads * self.activations).sum(dim=1).squeeze().cpu().numpy()
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (inputs.shape[-1], inputs.shape[-2]))
        return cam / (cam.max() + 1e-8)


def overlay_heatmap(image: np.ndarray, cam: np.ndarray) -> np.ndarray:
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    overlay = (0.55 * image + 0.45 * heatmap).clip(0, 255).astype(np.uint8)
    return overlay


def save_gradcam_artifacts(image: np.ndarray, cam: np.ndarray, output_path: Path) -> Path:
    overlay = overlay_heatmap(image, cam)
    Image.fromarray(overlay).save(output_path)
    return output_path
