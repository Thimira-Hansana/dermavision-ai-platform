"""Structured logging helpers."""

from __future__ import annotations

import sys

from loguru import logger


def configure_logging() -> None:
    """Configure Loguru once for console output."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="INFO",
        enqueue=True,
    )


__all__ = ["configure_logging", "logger"]
