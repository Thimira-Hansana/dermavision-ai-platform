"""Evaluation entry point."""

from __future__ import annotations

from pathlib import Path

from torch.utils.data import DataLoader

from dermavision_ai.core.constants import CLASS_ORDER
from dermavision_ai.core.logging import configure_logging
from dermavision_ai.core.settings import get_settings
from dermavision_ai.core.utils import get_device
from dermavision_ai.data.dataset import DatasetConfig, SkinLesionDataset, create_splits
from dermavision_ai.evaluation.reports import evaluate_model, export_confusion_matrix
from dermavision_ai.models.model_factory import build_model, load_checkpoint


def main() -> None:
    configure_logging()
    settings = get_settings()
    frame = create_splits(DatasetConfig())
    dataset = SkinLesionDataset(frame, "test", DatasetConfig())
    loader = DataLoader(dataset, batch_size=16)
    checkpoint = sorted(settings.model_dir.glob("*.pt"))
    if not checkpoint:
        raise FileNotFoundError("No checkpoint found under models/checkpoints.")
    model = build_model(settings.default_model, num_classes=len(CLASS_ORDER), pretrained=False)
    load_checkpoint(model, checkpoint[-1])
    device = get_device()
    model.to(device)
    results = evaluate_model(model, loader, device)
    figure = export_confusion_matrix(
        results["targets"],
        results["predictions"],
        Path("reports/figures"),
    )
    print({"metrics": results["metrics"], "confusion_matrix": str(figure)})


if __name__ == "__main__":
    main()
