"""Upload validation."""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from dermavision_ai.core.settings import get_settings


async def validate_upload(file: UploadFile) -> bytes:
    settings = get_settings()
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in settings.parsed_allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type.",
        )
    payload = await file.read()
    limit = settings.max_upload_mb * 1024 * 1024
    if len(payload) > limit:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds size limit.",
        )
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty upload.")
    return payload
