from __future__ import annotations

from pathlib import Path
from uuid import uuid4

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


def test_preprocess_image_resizes() -> None:
    temp_dir = Path(".tmp") / "test-artifacts"
    temp_dir.mkdir(parents=True, exist_ok=True)
    image_path = temp_dir / f"{uuid4().hex}.jpg"
    try:
        Image.new("RGB", (320, 240), color=(200, 50, 50)).save(image_path)
        result = preprocess_image(image_path, None, PreprocessingConfig(image_size=128))
        assert result.shape == (128, 128, 3)
    finally:
        image_path.unlink(missing_ok=True)
