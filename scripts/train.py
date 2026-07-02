"""Training entry point."""

from __future__ import annotations

from dermavision_ai.core.logging import configure_logging
from dermavision_ai.core.settings import get_settings
from dermavision_ai.core.utils import get_device, seed_everything
from dermavision_ai.training.engine import TrainerConfig, train_model


def main() -> None:
    configure_logging()
    settings = get_settings()
    config = settings.load_yaml_config()
    seed_everything(int(config.get("dataset", {}).get("random_seed", 42)))
    result = train_model(
        TrainerConfig(
            model_name=str(config.get("training", {}).get("model_name", settings.default_model)),
            image_size=int(config.get("dataset", {}).get("image_size", 224)),
            batch_size=int(config.get("dataset", {}).get("batch_size", 16)),
            num_workers=int(config.get("dataset", {}).get("num_workers", 2)),
            epochs=int(config.get("training", {}).get("epochs", 5)),
            learning_rate=float(config.get("training", {}).get("learning_rate", 3e-4)),
            weight_decay=float(config.get("training", {}).get("weight_decay", 1e-4)),
            optimizer=str(config.get("training", {}).get("optimizer", "adamw")),
            scheduler=str(config.get("training", {}).get("scheduler", "cosine")),
            loss_name=str(config.get("training", {}).get("loss", "focal")),
            sampler=str(config.get("training", {}).get("sampler", "weighted")),
            mixed_precision=bool(config.get("training", {}).get("mixed_precision", True)),
            gradient_clip=float(config.get("training", {}).get("gradient_clip", 1.0)),
            early_stopping_patience=int(config.get("training", {}).get("early_stopping_patience", 3)),
            checkpoints_dir=settings.model_dir,
            mlflow_tracking_uri=settings.mlflow_tracking_uri,
        ),
        device=get_device(),
    )
    print(result)


if __name__ == "__main__":
    main()
