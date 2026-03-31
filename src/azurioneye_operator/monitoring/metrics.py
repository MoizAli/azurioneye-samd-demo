"""
Performance metrics for monitoring and regulatory evidence.

Implements: REQ-005 (latency monitoring), RM-004 (performance degradation detection)

Tracks:
  - Inference latency (p50, p95, p99)
  - Request count by endpoint
  - Error rates
  - Model prediction distribution

Design Reference: SADD Section 3.3 - Monitoring
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List
import statistics


class MetricsCollector:
    """In-memory metrics collector for demo purposes."""

    def __init__(self):
        self._latencies: List[float] = []
        self._request_counts: Dict[str, int] = defaultdict(int)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._predictions: Dict[str, int] = defaultdict(int)

    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self._latencies.append(latency_ms)
        self._request_counts[endpoint] += 1

    def record_error(self, endpoint: str, error_type: str) -> None:
        self._error_counts[f"{endpoint}:{error_type}"] += 1

    def record_prediction(self, classification: str) -> None:
        self._predictions[classification] += 1

    def get_latency_stats(self) -> dict:
        if not self._latencies:
            return {"p50": 0, "p95": 0, "p99": 0, "count": 0}
        sorted_lat = sorted(self._latencies)
        n = len(sorted_lat)
        return {
            "p50": sorted_lat[int(n * 0.5)],
            "p95": sorted_lat[int(n * 0.95)] if n > 20 else sorted_lat[-1],
            "p99": sorted_lat[int(n * 0.99)] if n > 100 else sorted_lat[-1],
            "mean": round(statistics.mean(sorted_lat), 2),
            "count": n,
        }

    def get_summary(self) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency": self.get_latency_stats(),
            "requests": dict(self._request_counts),
            "errors": dict(self._error_counts),
            "predictions": dict(self._predictions),
        }
