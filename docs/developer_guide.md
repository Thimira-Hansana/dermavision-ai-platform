# Developer Guide

- Run `ruff check .` and `pytest` before committing.
- Backend code should keep ML logic inside `src/dermavision_ai/`, not inside route handlers.
- Frontend pages should call `frontend/src/services/api.ts` rather than making inline HTTP calls.
