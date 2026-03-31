"""
Clinical workflow orchestration endpoints.

Implements:
  - REQ-006: System shall orchestrate clinical workflow state transitions
  - REQ-007: System shall validate workflow transitions against allowed state machine
  - REQ-008: System shall emit events on state transitions for downstream consumers

Risk Mitigation:
  - RM-001: Invalid clinical state transition (mitigated by state machine validation)
  - RM-002: Lost workflow context (mitigated by persistent state + audit log)

Design Reference: SADD Section 4.1 - Orchestration Engine
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import logging

from ..core.orchestrator import WorkflowOrchestrator
from ..core.state_manager import WorkflowState
from ..infra.audit_logger import AuditLogger

router = APIRouter()
logger = logging.getLogger(__name__)
audit = AuditLogger()
orchestrator = WorkflowOrchestrator()


class ProcedureType(str, Enum):
    PCI = "pci"
    DIAGNOSTIC_ANGIO = "diagnostic_angio"
    STRUCTURAL_HEART = "structural_heart"


class WorkflowStartRequest(BaseModel):
    """Request to start a new clinical workflow."""
    procedure_type: ProcedureType
    patient_id: str = Field(..., min_length=1, max_length=64, description="Anonymized patient identifier")
    operator_id: str = Field(..., min_length=1, description="Clinician identifier")
    lab_id: str = Field(default="cath-lab-01", description="Cath lab identifier")


class WorkflowTransitionRequest(BaseModel):
    """Request to transition workflow to next state."""
    workflow_id: str
    target_state: str
    reason: Optional[str] = None


@router.post("/start")
async def start_workflow(request: WorkflowStartRequest):
    """
    Start a new clinical workflow (REQ-006).
    Creates workflow instance, initializes state machine, logs to audit trail.
    """
    workflow = orchestrator.create_workflow(
        procedure_type=request.procedure_type.value,
        patient_id=request.patient_id,
        operator_id=request.operator_id,
        lab_id=request.lab_id,
    )

    audit.log(
        event="workflow_started",
        workflow_id=workflow["id"],
        procedure_type=request.procedure_type.value,
        operator_id=request.operator_id,
        clinical_decision=True,
    )

    return workflow


@router.post("/transition")
async def transition_workflow(request: WorkflowTransitionRequest):
    """
    Transition workflow to a new state (REQ-007).
    Validates transition against state machine before applying.
    Emits event on successful transition (REQ-008).
    """
    try:
        result = orchestrator.transition(
            workflow_id=request.workflow_id,
            target_state=request.target_state,
        )
    except ValueError as e:
        # RM-001: Invalid state transition caught and logged
        audit.log(
            event="invalid_transition_attempted",
            workflow_id=request.workflow_id,
            target_state=request.target_state,
            error=str(e),
            safety_critical=True,
        )
        raise HTTPException(status_code=400, detail=str(e))

    audit.log(
        event="workflow_transitioned",
        workflow_id=request.workflow_id,
        new_state=request.target_state,
        clinical_decision=True,
    )

    return result


@router.get("/status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get current workflow state and history (REQ-006)."""
    status = orchestrator.get_status(workflow_id)
    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return status
