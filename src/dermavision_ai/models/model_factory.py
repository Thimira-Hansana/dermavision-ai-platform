"""Model loading helpers."""

from __future__ import annotations

from pathlib import Path

import torch
from torch import nn

from dermavision_ai.models.classifier import ModelSpec, create_classifier


def build_model(
    model_name: str,
    num_classes: int,
    pretrained: bool = True,
    dropout: float = 0.3,
) -> nn.Module:
    return create_classifier(
        ModelSpec(
            name=model_name,
            pretrained=pretrained,
            num_classes=num_classes,
            dropout=dropout,
        )
    )


def load_checkpoint(model: nn.Module, checkpoint_path: Path, map_location: str = "cpu") -> dict:
    checkpoint = torch.load(checkpoint_path, map_location=map_location)
    state_dict = checkpoint["model_state_dict"] if "model_state_dict" in checkpoint else checkpoint
    model.load_state_dict(state_dict)
    return checkpoint
