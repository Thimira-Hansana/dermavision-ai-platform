"""Optional segmentation pipeline utilities."""

from __future__ import annotations

from dermavision_ai.data.discovery import resolve_dataset_paths


def segmentation_available() -> bool:
    try:
        paths = resolve_dataset_paths()
    except FileNotFoundError:
        return False
    return len(paths.segmentation_dirs) > 0


def describe_segmentation_status() -> dict[str, str | bool | list[str]]:
    try:
        paths = resolve_dataset_paths()
    except FileNotFoundError:
        return {"available": False, "message": "Dataset not found.", "directories": []}
    directories = [str(path) for path in paths.segmentation_dirs]
    if not directories:
        return {
            "available": False,
            "message": "Segmentation masks were not detected; segmentation-assisted cropping is disabled.",
            "directories": [],
        }
    return {
        "available": True,
        "message": "Segmentation masks detected and supported by preprocessing.",
        "directories": directories,
    }
