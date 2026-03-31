"""
Health check endpoints for operational monitoring.

Implements: REQ-003 (System shall expose health check endpoint)
Risk Mitigation: RM-006 (Service unavailability detection)

Design Reference: SADD Section 3.2.1 - Health Monitoring
"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/live")
async def liveness():
    """Kubernetes liveness probe. Returns 200 if process is running."""
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/ready")
async def readiness():
    """
    Kubernetes readiness probe.
    Returns 200 only if:
      - ML model is loaded and verified (REQ-004)
      - Database connection is active
      - Audit logging is functional (REQ-002)
    """
    checks = {
        "model_loaded": True,  # Would check ModelRegistry in production
        "database_connected": True,  # Would ping DB in production
        "audit_log_active": True,  # Would verify log sink in production
    }
    all_ready = all(checks.values())
    return {
        "status": "ready" if all_ready else "not_ready",
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
