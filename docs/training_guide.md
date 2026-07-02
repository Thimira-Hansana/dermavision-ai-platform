# Training Guide

1. Install dependencies with `poetry install`.
2. Confirm the HAM10000 dataset is present under `data/`.
3. Adjust `configs/config.yaml` if needed.
4. Run `poetry run dermavision-train`.
5. Review checkpoints in `models/checkpoints/` and MLflow runs under `mlruns/`.
