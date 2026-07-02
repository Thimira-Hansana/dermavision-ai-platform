"""Classifier model wrappers."""

from __future__ import annotations

from dataclasses import dataclass

import timm
import torch
from torch import nn


class BaselineCNN(nn.Module):
    """Compact baseline CNN used for smoke tests and benchmarking."""

    def __init__(self, num_classes: int, dropout: float = 0.3) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(inputs))


@dataclass(slots=True)
class ModelSpec:
    name: str
    pretrained: bool
    num_classes: int
    dropout: float = 0.3


def create_classifier(spec: ModelSpec) -> nn.Module:
    if spec.name == "baseline_cnn":
        return BaselineCNN(num_classes=spec.num_classes, dropout=spec.dropout)
    return timm.create_model(
        spec.name,
        pretrained=spec.pretrained,
        num_classes=spec.num_classes,
        drop_rate=spec.dropout,
    )
