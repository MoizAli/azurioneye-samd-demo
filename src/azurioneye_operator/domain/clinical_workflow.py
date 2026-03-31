"""
Clinical workflow domain model.

Defines the domain objects for interventional cardiology procedures.
These models represent the clinical context that flows through the
orchestration engine.

Design Reference: SADD Section 3.1 - Domain Model
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProcedureType(str, Enum):
    """Supported interventional cardiology procedure types."""
    PCI = "pci"
    DIAGNOSTIC_ANGIO = "diagnostic_angio"
    STRUCTURAL_HEART = "structural_heart"


class ClinicalPhase(str, Enum):
    """Clinical phases within a procedure."""
    TIMEOUT = "timeout"
    ACCESS = "access"
    DIAGNOSTIC = "diagnostic"
    INTERVENTION = "intervention"
    CLOSURE = "closure"


class PatientContext(BaseModel):
    """Anonymized patient context for workflow orchestration."""
    patient_id: str = Field(..., description="Anonymized patient identifier")
    procedure_type: ProcedureType
    lab_id: str = Field(default="cath-lab-01")
    operator_id: str = Field(..., description="Primary operator/clinician")
    clinical_notes: Optional[str] = None


class WorkflowEvent(BaseModel):
    """Event emitted on workflow state transitions (REQ-008)."""
    event_id: str
    workflow_id: str
    event_type: str
    timestamp: datetime
    source_state: str
    target_state: str
    metadata: dict = Field(default_factory=dict)
