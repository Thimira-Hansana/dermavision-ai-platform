"""Settings management."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dermavision_ai.core.constants import ROOT_DIR


class Settings(BaseSettings):
    """Runtime settings sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="DERMAVISION_",
        env_file=".env",
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    env: str = Field(default="development")
    data_dir: Path = Field(default=ROOT_DIR / "data")
    config_path: Path = Field(default=ROOT_DIR / "configs" / "config.yaml")
    database_url: str = Field(default="sqlite+aiosqlite:///./dermavision.db")
    model_dir: Path = Field(default=ROOT_DIR / "models" / "checkpoints")
    default_model: str = Field(default="efficientnet_b0")
    model_checkpoint: str | None = Field(default=None)
    max_upload_mb: int = Field(default=10)
    allowed_extensions: str = Field(default=".png,.jpg,.jpeg")
    mlflow_tracking_uri: str = Field(default="mlruns")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    @property
    def parsed_allowed_extensions(self) -> list[str]:
        return [item.strip().lower() for item in self.allowed_extensions.split(",") if item.strip()]

    def load_yaml_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with self.config_path.open("r", encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
        return loaded if isinstance(loaded, dict) else {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
