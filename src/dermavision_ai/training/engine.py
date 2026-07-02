"""Training and validation loops."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mlflow
import torch
from loguru import logger
from torch import nn
from torch.optim import AdamW, Optimizer
from torch.optim.lr_scheduler import CosineAnnealingLR, ReduceLROnPlateau, _LRScheduler
from torch.utils.data import DataLoader, WeightedRandomSampler

from dermavision_ai.core.constants import CLASS_ORDER
from dermavision_ai.core.utils import ensure_directory
from dermavision_ai.data.dataset import (
    DatasetConfig,
    SkinLesionDataset,
    compute_class_weights,
    compute_sample_weights,
    create_splits,
)
from dermavision_ai.models.model_factory import build_model
from dermavision_ai.training.losses import build_loss
from dermavision_ai.training.metrics import classification_metrics


@dataclass(slots=True)
class TrainerConfig:
    model_name: str = "efficientnet_b0"
    image_size: int = 224
    batch_size: int = 16
    num_workers: int = 2
    epochs: int = 5
    learning_rate: float = 3e-4
    weight_decay: float = 1e-4
    dropout: float = 0.3
    optimizer: str = "adamw"
    scheduler: str = "cosine"
    loss_name: str = "focal"
    sampler: str = "weighted"
    mixed_precision: bool = True
    gradient_clip: float = 1.0
    early_stopping_patience: int = 3
    checkpoints_dir: Path = Path("models/checkpoints")
    mlflow_tracking_uri: str = "mlruns"


def _build_optimizer(parameters: Any, config: TrainerConfig) -> Optimizer:
    return AdamW(parameters, lr=config.learning_rate, weight_decay=config.weight_decay)


def _build_scheduler(optimizer: Optimizer, config: TrainerConfig) -> _LRScheduler | ReduceLROnPlateau:
    if config.scheduler == "plateau":
        return ReduceLROnPlateau(optimizer, mode="max", patience=1, factor=0.5)
    return CosineAnnealingLR(optimizer, T_max=max(config.epochs, 1))


def _make_loaders(config: TrainerConfig) -> tuple[dict[str, DataLoader[Any]], torch.Tensor]:
    split_frame = create_splits(
        DatasetConfig(
            image_size=config.image_size,
            use_clahe=True,
            use_segmentation_crop=True,
        )
    )
    datasets = {
        split: SkinLesionDataset(split_frame, split, DatasetConfig(image_size=config.image_size))
        for split in ("train", "val", "test")
    }
    sample_weights = compute_sample_weights(split_frame)
    class_weights = compute_class_weights(split_frame)
    sampler = (
        WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)
        if config.sampler == "weighted"
        else None
    )
    loaders = {
        "train": DataLoader(
            datasets["train"],
            batch_size=config.batch_size,
            num_workers=config.num_workers,
            sampler=sampler,
            shuffle=sampler is None,
        ),
        "val": DataLoader(datasets["val"], batch_size=config.batch_size, num_workers=config.num_workers),
        "test": DataLoader(datasets["test"], batch_size=config.batch_size, num_workers=config.num_workers),
    }
    return loaders, class_weights


def _run_epoch(
    model: nn.Module,
    loader: DataLoader[Any],
    criterion: nn.Module,
    device: torch.device,
    optimizer: Optimizer | None,
    scaler: torch.cuda.amp.GradScaler | None,
    gradient_clip: float,
) -> dict[str, Any]:
    is_train = optimizer is not None
    model.train(is_train)
    running_loss = 0.0
    predictions: list[int] = []
    targets: list[int] = []

    for batch in loader:
        inputs = batch["image"].to(device)
        labels = batch["label"].to(device)
        if is_train:
            optimizer.zero_grad(set_to_none=True)
        autocast_enabled = scaler is not None and device.type == "cuda"
        with torch.autocast(device_type=device.type, enabled=autocast_enabled):
            logits = model(inputs)
            loss = criterion(logits, labels)
        if is_train and optimizer is not None:
            if scaler is not None and device.type == "cuda":
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
                scaler.step(optimizer)
                scaler.update()
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip)
                optimizer.step()
        running_loss += loss.item() * inputs.size(0)
        predictions.extend(logits.argmax(dim=1).detach().cpu().tolist())
        targets.extend(labels.detach().cpu().tolist())

    metrics = classification_metrics(targets, predictions)
    metrics["loss"] = running_loss / max(len(loader.dataset), 1)
    return metrics


def train_model(config: TrainerConfig, device: torch.device) -> dict[str, Any]:
    """Train a classifier and save the best checkpoint."""
    ensure_directory(config.checkpoints_dir)
    loaders, class_weights = _make_loaders(config)
    model = build_model(config.model_name, num_classes=len(CLASS_ORDER), pretrained=True, dropout=config.dropout).to(device)
    criterion = build_loss(config.loss_name, class_weights.to(device))
    optimizer = _build_optimizer(model.parameters(), config)
    scheduler = _build_scheduler(optimizer, config)
    scaler = torch.cuda.amp.GradScaler() if config.mixed_precision and device.type == "cuda" else None
    best_score = float("-inf")
    patience = 0
    best_path = config.checkpoints_dir / f"{config.model_name}_best.pt"
    history: list[dict[str, float]] = []

    mlflow.set_tracking_uri(config.mlflow_tracking_uri)
    experiment = mlflow.set_experiment("dermavision-training")
    logger.info("Using MLflow experiment {}", experiment.name)

    with mlflow.start_run(run_name=config.model_name):
        mlflow.log_params(config.__dict__)
        for epoch in range(1, config.epochs + 1):
            train_metrics = _run_epoch(
                model,
                loaders["train"],
                criterion,
                device,
                optimizer,
                scaler,
                config.gradient_clip,
            )
            val_metrics = _run_epoch(
                model,
                loaders["val"],
                criterion,
                device,
                optimizer=None,
                scaler=None,
                gradient_clip=config.gradient_clip,
            )
            row = {f"train_{key}": value for key, value in train_metrics.items()}
            row.update({f"val_{key}": value for key, value in val_metrics.items()})
            row["epoch"] = float(epoch)
            history.append(row)
            mlflow.log_metrics(row, step=epoch)
            score = val_metrics["f1_macro"]
            if score > best_score:
                best_score = score
                patience = 0
                torch.save(
                    {
                        "model_state_dict": model.state_dict(),
                        "model_name": config.model_name,
                        "class_order": CLASS_ORDER,
                        "epoch": epoch,
                        "val_metrics": val_metrics,
                    },
                    best_path,
                )
            else:
                patience += 1
            if isinstance(scheduler, ReduceLROnPlateau):
                scheduler.step(score)
            else:
                scheduler.step()
            logger.info("Epoch {} train={} val={}", epoch, train_metrics, val_metrics)
            if patience >= config.early_stopping_patience:
                logger.info("Early stopping triggered at epoch {}", epoch)
                break

    return {
        "checkpoint_path": str(best_path),
        "best_f1_macro": best_score,
        "history": history,
    }
