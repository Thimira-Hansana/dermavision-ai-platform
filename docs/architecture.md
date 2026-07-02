# Architecture

DermaVision AI follows a clean-architecture layout:

- `src/dermavision_ai/` contains reusable domain, data, training, evaluation, inference, and explainability logic.
- `backend/` exposes the FastAPI application, async persistence, metrics, and HTTP-facing validation.
- `frontend/` provides the React operator interface for predictions, history, and runtime inspection.
- `configs/`, `scripts/`, `reports/`, and `docs/` hold runtime configuration, CLI entry points, generated assets, and project documentation.

Inference flow:

1. Client uploads an image through the React UI or API.
2. FastAPI validates file type and size.
3. `InferenceService` preprocesses the image and runs the classifier.
4. Grad-CAM generates a heatmap artifact.
5. The API persists history to SQLite and returns structured results.
