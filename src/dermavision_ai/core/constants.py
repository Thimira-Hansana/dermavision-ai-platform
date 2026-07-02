"""Project-wide constants."""

from __future__ import annotations

from pathlib import Path

CLASS_LABELS: dict[str, str] = {
    "akiec": "Actinic keratoses and intraepithelial carcinoma",
    "bcc": "Basal cell carcinoma",
    "bkl": "Benign keratosis-like lesions",
    "df": "Dermatofibroma",
    "mel": "Melanoma",
    "nv": "Melanocytic nevi",
    "vasc": "Vascular lesions",
}

CLASS_ORDER: list[str] = list(CLASS_LABELS)
SUPPORTED_IMAGE_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")
ROOT_DIR = Path(__file__).resolve().parents[3]
