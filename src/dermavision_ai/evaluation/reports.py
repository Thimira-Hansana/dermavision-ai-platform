"""Evaluation and figure export."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from sklearn.metrics import confusion_matrix, roc_auc_score
from torch.utils.data import DataLoader

from dermavision_ai.core.constants import CLASS_ORDER
from dermavision_ai.core.utils import ensure_directory
from dermavision_ai.training.metrics import build_classification_report, classification_metrics


def evaluate_model(
    model: torch.nn.Module,
    loader: DataLoader[Any],
    device: torch.device,
) -> dict[str, Any]:
    model.eval()
    predictions: list[int] = []
    targets: list[int] = []
    probabilities: list[np.ndarray] = []
    with torch.no_grad():
        for batch in loader:
            logits = model(batch["image"].to(device))
            probs = torch.softmax(logits, dim=1).cpu().numpy()
            probabilities.extend(probs)
            predictions.extend(logits.argmax(dim=1).cpu().tolist())
            targets.extend(batch["label"].cpu().tolist())
    metrics = classification_metrics(targets, predictions)
    report = build_classification_report(targets, predictions, CLASS_ORDER)
    try:
        metrics["roc_auc_ovr"] = float(
            roc_auc_score(targets, np.array(probabilities), multi_class="ovr", average="macro")
        )
    except ValueError:
        metrics["roc_auc_ovr"] = 0.0
    return {"metrics": metrics, "report": report, "targets": targets, "predictions": predictions}


def export_confusion_matrix(
    targets: list[int],
    predictions: list[int],
    output_dir: Path,
) -> Path:
    ensure_directory(output_dir)
    matrix = confusion_matrix(targets, predictions, labels=list(range(len(CLASS_ORDER))))
    figure, axis = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="YlOrBr", xticklabels=CLASS_ORDER, yticklabels=CLASS_ORDER, ax=axis)
    axis.set_title("Confusion Matrix")
    axis.set_xlabel("Predicted")
    axis.set_ylabel("Actual")
    output_path = output_dir / "confusion_matrix.png"
    figure.tight_layout()
    figure.savefig(output_path)
    plt.close(figure)
    return output_path
