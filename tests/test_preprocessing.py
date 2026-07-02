from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from dermavision_ai.data.preprocessing import (
    PreprocessingConfig,
    preprocess_image,
    validate_image_quality,
)


def test_validate_image_quality_accepts_rgb_images() -> None:
    image = np.zeros((224, 224, 3), dtype=np.uint8)
    image[:, :112] = 20
    image[:, 112:] = 220
    assert bool(validate_image_quality(image)) is True


def test_preprocess_image_resizes(tmp_path: Path) -> None:
    image_path = tmp_path / "test.jpg"
    Image.new("RGB", (320, 240), color=(200, 50, 50)).save(image_path)
    result = preprocess_image(image_path, None, PreprocessingConfig(image_size=128))
    assert result.shape == (128, 128, 3)
