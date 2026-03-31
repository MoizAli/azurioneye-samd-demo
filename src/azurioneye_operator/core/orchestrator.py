"""
Core workflow orchestration engine.

Implements:
  - REQ-006: Clinical workflow state management
  - REQ-007: State transition validation against allowed transitions
  - REQ-008: Event emission on state changes

Design Reference: SADD Section 4.1 - Orchestration Engine
Architecture Decision: Rule-based routing, non-SaMD orchestrator from the start.
  Re-certification question is what triggers it on changes, not when non-SaMD
  status is achieved.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from .state_manager import StateMachine, WorkflowState


class WorkflowOrchestrator:
    """
    Manages clinical workflow lifecycle.
    Each workflow has a unique ID and follows a defined state machine.
    """

    def __init__(self):
        self._workflows: Dict[str, dict] = {}

    def create_workflow(
        self,
        procedure_type: str,
        patient_id: str,
        operator_id: str,
        lab_id: str,
    ) -> dict:
        """Create a new workflow instance with initialized state machine."""
        workflow_id = f"WF-{uuid.uuid4().hex[:8].upper()}"
        state_machine = StateMachine()

        workflow = {
            "id": workflow_id,
            "procedure_type": procedure_type,
            "patient_id": patient_id,
            "operator_id": operator_id,
            "lab_id": lab_id,
            "state": state_machine.current_state.value,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "history": [
                {
                    "state": state_machine.current_state.value,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "action": "created",
                }
            ],
        }

        self._workflows[workflow_id] = {
            "data": workflow,
            "state_machine": state_machine,
        }

        return workflow

    def transition(self, workflow_id: str, target_state: str) -> dict:
        """
        Transition workflow to a new state (REQ-007).
        Raises ValueError if transition is not allowed.
        """
        if workflow_id not in self._workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        wf = self._workflows[workflow_id]
        state_machine: StateMachine = wf["state_machine"]

        try:
            target = WorkflowState(target_state)
        except ValueError:
            raise ValueError(
                f"Invalid state: {target_state}. "
                f"Valid states: {[s.value for s in WorkflowState]}"
            )

        if not state_machine.can_transition(target):
            raise ValueError(
                f"Cannot transition from {state_machine.current_state.value} "
                f"to {target_state}. Allowed: "
                f"{[s.value for s in state_machine.allowed_transitions()]}"
            )

        state_machine.transition(target)

        wf["data"]["state"] = target_state
        wf["data"]["updated_at"] = datetime.now(timezone.utc).isoformat()
        wf["data"]["history"].append(
            {
                "state": target_state,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "transitioned",
            }
        )

        return wf["data"]

    def get_status(self, workflow_id: str) -> Optional[dict]:
        """Get current workflow data including state and history."""
        wf = self._workflows.get(workflow_id)
        return wf["data"] if wf else None
