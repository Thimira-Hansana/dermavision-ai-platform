# API Guide

Endpoints:

- `GET /health`
- `GET /version`
- `GET /model-info`
- `GET /metrics`
- `GET /history`
- `POST /predict`
- `POST /predict/batch`

`POST /predict` expects multipart form data with a `file` field containing a PNG or JPEG image up to the configured size limit.
