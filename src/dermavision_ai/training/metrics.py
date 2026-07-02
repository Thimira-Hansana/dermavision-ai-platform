"""Metric computation helpers."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)


def classification_metrics(targets: list[int], predictions: list[int]) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(targets, predictions)),
        "precision_macro": float(precision_score(targets, predictions, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(targets, predictions, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(targets, predictions, average="macro", zero_division=0)),
    }


def build_classification_report(targets: list[int], predictions: list[int], labels: list[str]) -> dict[str, Any]:
    return classification_report(
        targets,
        predictions,
        target_names=labels,
        zero_division=0,
        output_dict=True,
    )


def top_k_predictions(probabilities: np.ndarray, labels: list[str], top_k: int = 3) -> list[dict[str, float | str]]:
    indices = np.argsort(probabilities)[::-1][:top_k]
    return [{"class": labels[index], "confidence": float(probabilities[index])} for index in indices]
