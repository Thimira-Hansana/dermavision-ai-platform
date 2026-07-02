"""PyTorch datasets and split utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import StratifiedShuffleSplit
from torch.utils.data import Dataset

from dermavision_ai.core.constants import CLASS_ORDER
from dermavision_ai.data.augmentation import build_eval_transforms, build_train_transforms
from dermavision_ai.data.discovery import load_metadata
from dermavision_ai.data.preprocessing import PreprocessingConfig, preprocess_image


@dataclass(slots=True)
class DatasetConfig:
    image_size: int = 224
    val_size: float = 0.15
    test_size: float = 0.15
    seed: int = 42
    use_clahe: bool = True
    use_segmentation_crop: bool = True


def create_splits(config: DatasetConfig) -> pd.DataFrame:
    """Create train/val/test split while keeping lesion groups together."""
    frame = load_metadata()
    lesions = frame[["lesion_id", "dx"]].drop_duplicates().reset_index(drop=True)
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=config.test_size, random_state=config.seed)
    train_val_idx, test_idx = next(splitter.split(lesions["lesion_id"], lesions["dx"]))
    train_val = lesions.iloc[train_val_idx].reset_index(drop=True)
    test = lesions.iloc[test_idx].reset_index(drop=True)

    adjusted_val_size = config.val_size / (1.0 - config.test_size)
    val_splitter = StratifiedShuffleSplit(n_splits=1, test_size=adjusted_val_size, random_state=config.seed)
    train_idx, val_idx = next(val_splitter.split(train_val["lesion_id"], train_val["dx"]))
    train = train_val.iloc[train_idx]
    val = train_val.iloc[val_idx]

    split_map = dict.fromkeys(train["lesion_id"], "train")
    split_map.update(dict.fromkeys(val["lesion_id"], "val"))
    split_map.update(dict.fromkeys(test["lesion_id"], "test"))
    frame["split"] = frame["lesion_id"].map(split_map)
    frame["label_index"] = frame["dx"].apply(CLASS_ORDER.index)
    return frame


class SkinLesionDataset(Dataset[dict[str, Any]]):
    """Dataset yielding tensors and metadata."""

    def __init__(
        self,
        frame: pd.DataFrame,
        split: str,
        config: DatasetConfig,
    ) -> None:
        self.frame = frame[frame["split"] == split].reset_index(drop=True)
        self.split = split
        self.preprocess_config = PreprocessingConfig(
            image_size=config.image_size,
            use_clahe=config.use_clahe,
            use_segmentation_crop=config.use_segmentation_crop,
        )
        self.transform = (
            build_train_transforms(config.image_size)
            if split == "train"
            else build_eval_transforms(config.image_size)
        )

    def __len__(self) -> int:
        return len(self.frame)

    def __getitem__(self, index: int) -> dict[str, Any]:
        row = self.frame.iloc[index]
        mask_value = row["mask_path"]
        image = preprocess_image(
            image_path=Path(row["image_path"]),
            mask_path=Path(mask_value) if isinstance(mask_value, (Path, str)) else None,
            config=self.preprocess_config,
        )
        transformed = self.transform(image=image)
        return {
            "image": transformed["image"],
            "label": torch.tensor(int(row["label_index"]), dtype=torch.long),
            "image_id": row["image_id"],
            "lesion_id": row["lesion_id"],
            "label_code": row["dx"],
            "label_name": row["label_name"],
        }


def compute_class_weights(frame: pd.DataFrame) -> torch.Tensor:
    counts = frame[frame["split"] == "train"]["label_index"].value_counts().sort_index()
    counts = counts.reindex(range(len(CLASS_ORDER)), fill_value=1)
    weights = 1.0 / counts.to_numpy(dtype=np.float32)
    normalized = weights / weights.sum() * len(CLASS_ORDER)
    return torch.tensor(normalized, dtype=torch.float32)


def compute_sample_weights(frame: pd.DataFrame) -> torch.Tensor:
    train_frame = frame[frame["split"] == "train"]
    counts = train_frame["label_index"].value_counts().sort_index().to_dict()
    weights = train_frame["label_index"].map(lambda label: 1.0 / counts[int(label)])
    return torch.tensor(weights.to_numpy(dtype=np.float32), dtype=torch.float32)
