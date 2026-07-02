"""Prometheus metrics registry."""

from __future__ import annotations

from prometheus_client import Counter, Histogram

prediction_counter = Counter(
    "dermavision_predictions_total",
    "Total number of predictions served.",
)
prediction_latency = Histogram(
    "dermavision_prediction_latency_ms",
    "Prediction latency in milliseconds.",
    buckets=(50, 100, 250, 500, 1000, 2000, 5000),
)
