"""
ML inference endpoints for cardiac rhythm classification.

Implements:
  - REQ-009: System shall classify cardiac rhythm from input signal data
  - REQ-010: System shall return classification with confidence score
  - REQ-011: System shall reject inputs that fail validation (REQ-004 derived)
  - REQ-012: Inference latency shall be <500ms (REQ-005 derived)

Risk Mitigation:
  - RM-003: Incorrect classification (mitigated by confidence threshold + human review)
  - RM-004: Performance degradation (mitigated by latency monitoring + alerting)

Design Reference: SADD Section 4.2 - Inference Pipeline
FDA PCCP Reference: Model versioning supports predetermined change control
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime, timezone
import logging
import time

from ..infra.audit_logger import AuditLogger

router = APIRouter()
logger = logging.getLogger(__name__)
audit = AuditLogger()

# Classification labels per AHA/ACC guidelines
RHYTHM_CLASSES = [
    "normal_sinus",
    "atrial_fibrillation",
    "atrial_flutter",
    "ventricular_tachycardia",
    "supraventricular_tachycardia",
    "bradycardia",
    "heart_block",
]

# Confidence threshold below which human review is required (RM-003)
CONFIDENCE_THRESHOLD = 0.85


class PredictionRequest(BaseModel):
    """Input for cardiac rhythm classification."""
    signal_data: List[float] = Field(
        ...,
        min_length=250,
        max_length=5000,
        description="ECG signal values (mV), minimum 250 samples at 250Hz = 1 second",
    )
    lead: str = Field(default="II", description="ECG lead (I, II, III, aVR, aVL, aVF, V1-V6)")
    sampling_rate_hz: int = Field(default=250, ge=100, le=1000)
    patient_id: Optional[str] = None
    workflow_id: Optional[str] = None

    @validator("lead")
    def validate_lead(cls, v):
        valid_leads = ["I", "II", "III", "aVR", "aVL", "aVF"] + [f"V{i}" for i in range(1, 7)]
        if v not in valid_leads:
            raise ValueError(f"Invalid ECG lead: {v}. Must be one of {valid_leads}")
        return v


class PredictionResponse(BaseModel):
    """Classification result with regulatory metadata."""
    classification: str
    confidence: float
    requires_human_review: bool
    model_version: str
    inference_time_ms: float
    timestamp: str
    signal_quality_score: float
    all_probabilities: dict


@router.post("/classify", response_model=PredictionResponse)
async def classify_rhythm(request: PredictionRequest):
    """
    Classify cardiac rhythm from ECG signal (REQ-009, REQ-010).

    Returns classification with confidence score. If confidence < 0.85,
    flags for mandatory human review (RM-003 mitigation).
    """
    start = time.monotonic()

    # Signal quality check (REQ-011)
    signal_quality = _assess_signal_quality(request.signal_data)
    if signal_quality < 0.3:
        audit.log(
            event="prediction_rejected",
            reason="poor_signal_quality",
            signal_quality=signal_quality,
            patient_id=request.patient_id,
            safety_critical=True,
        )
        raise HTTPException(
            status_code=422,
            detail=f"Signal quality too low ({signal_quality:.2f}). Minimum: 0.30",
        )

    # Dummy inference (in production, this calls the PyTorch model)
    probabilities = _dummy_inference(request.signal_data)
    top_class = max(probabilities, key=probabilities.get)
    top_confidence = probabilities[top_class]
    requires_review = top_confidence < CONFIDENCE_THRESHOLD

    inference_time_ms = (time.monotonic() - start) * 1000

    # Audit trail for every prediction (REQ-002)
    audit.log(
        event="prediction_made",
        classification=top_class,
        confidence=top_confidence,
        requires_human_review=requires_review,
        inference_time_ms=round(inference_time_ms, 2),
        model_version="1.0.0",
        patient_id=request.patient_id,
        workflow_id=request.workflow_id,
        clinical_decision=True,
    )

    # Latency check (REQ-012, RM-004)
    if inference_time_ms > 500:
        logger.warning(
            f"Inference latency exceeded threshold: {inference_time_ms:.0f}ms > 500ms",
            extra={"safety_critical": True},
        )

    return PredictionResponse(
        classification=top_class,
        confidence=round(top_confidence, 4),
        requires_human_review=requires_review,
        model_version="1.0.0",
        inference_time_ms=round(inference_time_ms, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
        signal_quality_score=round(signal_quality, 4),
        all_probabilities={k: round(v, 4) for k, v in probabilities.items()},
    )


def _assess_signal_quality(signal_data: List[float]) -> float:
    """
    Assess ECG signal quality (0.0 = noise, 1.0 = clean).
    Uses signal-to-noise ratio estimation.
    """
    if not signal_data:
        return 0.0
    mean_val = sum(signal_data) / len(signal_data)
    variance = sum((x - mean_val) ** 2 for x in signal_data) / len(signal_data)
    # Simple heuristic: physiological ECG signals have bounded variance
    if variance < 0.001 or variance > 100:
        return 0.2
    return min(1.0, 0.5 + (1.0 / (1.0 + abs(variance - 1.0))))


def _dummy_inference(signal_data: List[float]) -> dict:
    """
    Dummy inference function. Returns mock probabilities.
    In production, this calls the PyTorch model via ModelRegistry.
    """
    # Deterministic dummy: use signal mean to pick a class
    mean_val = sum(signal_data) / len(signal_data) if signal_data else 0
    import math
    base_idx = int(abs(mean_val * 100)) % len(RHYTHM_CLASSES)

    probs = {}
    remaining = 1.0
    for i, cls in enumerate(RHYTHM_CLASSES):
        if i == base_idx:
            probs[cls] = 0.91  # High confidence for demo
            remaining -= 0.91
        else:
            share = remaining / (len(RHYTHM_CLASSES) - 1) if i < len(RHYTHM_CLASSES) - 1 else remaining
            val = max(0.01, share * (0.5 + (i * 0.1)))
            probs[cls] = round(val, 4)
            remaining -= val

    # Normalize
    total = sum(probs.values())
    return {k: v / total for k, v in probs.items()}
