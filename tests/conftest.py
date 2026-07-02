from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image


@pytest.fixture()
def sample_image_bytes() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (224, 224), color=(120, 80, 60)).save(buffer, format="JPEG")
    return buffer.getvalue()
