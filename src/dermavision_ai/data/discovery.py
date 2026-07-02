"""Dataset discovery helpers for HAM10000."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from dermavision_ai.core.constants import CLASS_LABELS, ROOT_DIR
from dermavision_ai.core.settings import get_settings


@dataclass(slots=True)
class DatasetPaths:
    """Resolved dataset paths."""

    data_dir: Path
    metadata_path: Path
    image_dirs: list[Path]
    segmentation_dirs: list[Path]


def _candidate_data_dirs() -> list[Path]:
    settings = get_settings()
    direct = settings.data_dir
    candidates = [direct, direct / "archive", ROOT_DIR / "data", ROOT_DIR / "data" / "archive"]
    resolved: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        target = candidate.resolve()
        if target not in seen and target.exists():
            resolved.append(target)
            seen.add(target)
    return resolved


def resolve_dataset_paths() -> DatasetPaths:
    """Locate metadata, image folders, and optional segmentation folders."""
    for data_dir in _candidate_data_dirs():
        metadata_path = data_dir / "HAM10000_metadata.csv"
        if not metadata_path.exists():
            continue
        image_dirs = sorted(path for path in data_dir.glob("HAM10000_images_part_*") if path.is_dir())
        segmentation_dirs = sorted(
            path
            for path in data_dir.iterdir()
            if path.is_dir() and "segment" in path.name.lower()
        )
        if image_dirs:
            return DatasetPaths(
                data_dir=data_dir,
                metadata_path=metadata_path,
                image_dirs=image_dirs,
                segmentation_dirs=segmentation_dirs,
            )
    raise FileNotFoundError("HAM10000 dataset not found under the local data directory.")


def _build_image_index(image_dirs: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for directory in image_dirs:
        for path in directory.glob("*.jpg"):
            index[path.stem] = path
    return index


def _build_mask_index(mask_dirs: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for directory in mask_dirs:
        for extension in ("*.png", "*.jpg", "*.jpeg"):
            for path in directory.glob(extension):
                key = path.stem.replace("_segmentation", "").replace("_mask", "")
                index[key] = path
    return index


def load_metadata() -> pd.DataFrame:
    """Load metadata and attach resolved file paths."""
    paths = resolve_dataset_paths()
    frame = pd.read_csv(paths.metadata_path)
    frame["dx"] = frame["dx"].str.lower()
    frame = frame[frame["dx"].isin(CLASS_LABELS)].copy()
    image_index = _build_image_index(paths.image_dirs)
    mask_index = _build_mask_index(paths.segmentation_dirs)
    frame["image_path"] = frame["image_id"].map(image_index)
    frame["mask_path"] = frame["image_id"].map(mask_index)
    frame["label_name"] = frame["dx"].map(CLASS_LABELS)
    frame["has_mask"] = frame["mask_path"].notna()
    frame = frame.dropna(subset=["image_path"]).reset_index(drop=True)
    return frame
