# Deployment Guide

Local backend:

`poetry run uvicorn backend.main:app --reload`

Local frontend:

`cd frontend && npm install && npm run dev`

Docker Compose:

`docker compose up --build`
