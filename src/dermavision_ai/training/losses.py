"""Loss functions for imbalanced classification."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


class FocalLoss(nn.Module):
    """Multiclass focal loss."""

    def __init__(
        self,
        gamma: float = 2.0,
        weight: torch.Tensor | None = None,
    ) -> None:
        super().__init__()
        self.gamma = gamma
        self.register_buffer("weight", weight if weight is not None else None)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(logits, targets, weight=self.weight, reduction="none")
        probs = torch.exp(-ce_loss)
        return ((1 - probs) ** self.gamma * ce_loss).mean()


def build_loss(name: str, class_weights: torch.Tensor | None = None) -> nn.Module:
    if name == "focal":
        return FocalLoss(weight=class_weights)
    return nn.CrossEntropyLoss(weight=class_weights)
