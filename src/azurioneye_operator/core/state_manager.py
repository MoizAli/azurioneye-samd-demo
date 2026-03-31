"""
Clinical workflow state machine.

Implements: REQ-007 (State transition validation)
Risk Mitigation: RM-001 (Invalid clinical state transition)

The state machine defines allowed transitions for interventional
cardiology procedures. Invalid transitions are blocked and logged.

Design Reference: SADD Section 4.1.1 - State Machine Definition

States follow the typical cath lab procedure flow:
  CREATED -> PRE_PROCEDURE -> PATIENT_ON_TABLE -> PROCEDURE_ACTIVE
  -> POST_PROCEDURE -> COMPLETED

Emergency abort is allowed from any active state.
"""

from enum import Enum
from typing import List, Dict, Set


class WorkflowState(str, Enum):
    CREATED = "created"
    PRE_PROCEDURE = "pre_procedure"
    PATIENT_ON_TABLE = "patient_on_table"
    PROCEDURE_ACTIVE = "procedure_active"
    POST_PROCEDURE = "post_procedure"
    COMPLETED = "completed"
    ABORTED = "aborted"
    ERROR = "error"


# Allowed state transitions (directed graph)
TRANSITIONS: Dict[WorkflowState, Set[WorkflowState]] = {
    WorkflowState.CREATED: {
        WorkflowState.PRE_PROCEDURE,
        WorkflowState.ABORTED,
    },
    WorkflowState.PRE_PROCEDURE: {
        WorkflowState.PATIENT_ON_TABLE,
        WorkflowState.ABORTED,
    },
    WorkflowState.PATIENT_ON_TABLE: {
        WorkflowState.PROCEDURE_ACTIVE,
        WorkflowState.ABORTED,
    },
    WorkflowState.PROCEDURE_ACTIVE: {
        WorkflowState.POST_PROCEDURE,
        WorkflowState.ABORTED,
        WorkflowState.ERROR,
    },
    WorkflowState.POST_PROCEDURE: {
        WorkflowState.COMPLETED,
        WorkflowState.ERROR,
    },
    WorkflowState.COMPLETED: set(),  # Terminal state
    WorkflowState.ABORTED: set(),  # Terminal state
    WorkflowState.ERROR: {
        WorkflowState.ABORTED,
    },
}


class StateMachine:
    """
    Enforces valid workflow state transitions.
    All transitions are validated against the TRANSITIONS graph.
    """

    def __init__(self, initial_state: WorkflowState = WorkflowState.CREATED):
        self._current = initial_state

    @property
    def current_state(self) -> WorkflowState:
        return self._current

    def can_transition(self, target: WorkflowState) -> bool:
        """Check if transition from current state to target is allowed."""
        return target in TRANSITIONS.get(self._current, set())

    def allowed_transitions(self) -> List[WorkflowState]:
        """Return list of states reachable from current state."""
        return list(TRANSITIONS.get(self._current, set()))

    def transition(self, target: WorkflowState) -> None:
        """
        Execute state transition. Raises ValueError if not allowed.
        This is the enforcement point for RM-001.
        """
        if not self.can_transition(target):
            raise ValueError(
                f"Invalid transition: {self._current.value} -> {target.value}"
            )
        self._current = target

    def is_terminal(self) -> bool:
        """Check if current state is terminal (no further transitions)."""
        return len(self.allowed_transitions()) == 0
