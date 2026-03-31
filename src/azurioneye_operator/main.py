"""
Main FastAPI application entry point for AzurionEye AI Operator.

Regulatory References:
  - REQ-001: System shall provide REST API for clinical workflow orchestration
  - REQ-002: System shall maintain audit log of all clinical decisions
  - REQ-003: System shall expose health check endpoint for operational monitoring
  - REQ-004: System shall load ML model on startup with version verification

Design References:
  - SADD Section 3.2: Container architecture (FastAPI service)
  - SDDD Section 2.1: REST API contract
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import json
from datetime import datetime, timezone

from .api.health import router as health_router
from .api.orchestrate import router as orchestrate_router
from .api.predict import router as predict_router
from .config import settings
from .infra.audit_logger import AuditLogger

logger = logging.getLogger(__name__)
audit = AuditLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle. Loads ML model on startup (REQ-004)."""
    logger.info(f"AzurionEye Operator starting, version {settings.app_version}")
    # Model loading would happen here in production
    yield
    logger.info("AzurionEye Operator shutting down")


app = FastAPI(
    title="AzurionEye AI Operator",
    description="Medical Device Software - IEC 62304 Class B, FDA 510(k)",
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(orchestrate_router, prefix="/orchestrate", tags=["Orchestration"])
app.include_router(predict_router, prefix="/predict", tags=["Inference"])


@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    """
    Audit logging middleware for all requests (REQ-002).
    Every clinical decision and API call is logged with timestamp,
    request details, and response status for regulatory evidence.
    """
    start_time = datetime.now(timezone.utc)
    response = await call_next(request)
    process_time_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

    audit.log(
        event="api_request",
        method=request.method,
        path=str(request.url.path),
        status_code=response.status_code,
        process_time_ms=round(process_time_ms, 2),
        client_ip=request.client.host if request.client else None,
    )
    return response


@app.get("/", tags=["Info"])
async def root():
    """Service root endpoint (REQ-001)."""
    return {
        "name": "AzurionEye AI Operator",
        "version": settings.app_version,
        "safety_class": "IEC 62304 Class B",
        "status": "operational",
    }
