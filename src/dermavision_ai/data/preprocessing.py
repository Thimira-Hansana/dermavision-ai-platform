"""Preprocessing functions for dermoscopy images."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


@dataclass(slots=True)
class PreprocessingConfig:
    image_size: int = 224
    use_clahe: bool = True
    use_segmentation_crop: bool = True


def read_rgb_image(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.array(image.convert("RGB"))


def read_mask(path: Path | None) -> np.ndarray | None:
    if path is None or not path.exists():
        return None
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return None
    return mask


def apply_clahe(image: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l_channel)
    merged = cv2.merge((enhanced_l, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)


def crop_to_mask(image: np.ndarray, mask: np.ndarray | None) -> np.ndarray:
    if mask is None:
        return image
    thresholded = (mask > 0).astype(np.uint8)
    coordinates = cv2.findNonZero(thresholded)
    if coordinates is None:
        return image
    x, y, width, height = cv2.boundingRect(coordinates)
    return image[y : y + height, x : x + width]


def validate_image_quality(image: np.ndarray) -> bool:
    if image.ndim != 3 or image.shape[2] != 3:
        return False
    if image.shape[0] < 32 or image.shape[1] < 32:
        return False
    return image.std() > 5.0


def preprocess_image(
    image_path: Path,
    mask_path: Path | None,
    config: PreprocessingConfig,
) -> np.ndarray:
    image = read_rgb_image(image_path)
    if config.use_segmentation_crop:
        image = crop_to_mask(image, read_mask(mask_path))
    if config.use_clahe:
        image = apply_clahe(image)
    if not validate_image_quality(image):
        raise ValueError(f"Image at {image_path} failed quality checks.")
    resized = cv2.resize(image, (config.image_size, config.image_size), interpolation=cv2.INTER_AREA)
    return resized
