"""
Unit tests for clinical workflow state machine.

Verifies:
  - REQ-007: State transition validation
  - RM-001: Invalid clinical state transition prevention

Traceability:
  - TC-007.1: Valid forward transitions
  - TC-007.2: Invalid transitions are rejected
  - TC-007.3: Terminal states have no outgoing transitions
  - TC-007.4: Emergency abort available from all active states
  - TC-RM-001.1: Invalid transition raises ValueError
"""

import pytest
from src.azurioneye_operator.core.state_manager import (
    StateMachine,
    WorkflowState,
    TRANSITIONS,
)


class TestValidTransitions:
    """TC-007.1: Verify all valid forward transitions."""

    def test_created_to_pre_procedure(self, state_machine):
        """Normal flow: created -> pre_procedure."""
        assert state_machine.can_transition(WorkflowState.PRE_PROCEDURE)
        state_machine.transition(WorkflowState.PRE_PROCEDURE)
        assert state_machine.current_state == WorkflowState.PRE_PROCEDURE

    def test_full_happy_path(self, state_machine):
        """Complete procedure flow from creation to completion."""
        expected_flow = [
            WorkflowState.PRE_PROCEDURE,
            WorkflowState.PATIENT_ON_TABLE,
            WorkflowState.PROCEDURE_ACTIVE,
            WorkflowState.POST_PROCEDURE,
            WorkflowState.COMPLETED,
        ]
        for target in expected_flow:
            state_machine.transition(target)
        assert state_machine.current_state == WorkflowState.COMPLETED
        assert state_machine.is_terminal()

    def test_error_to_abort(self, state_machine):
        """Error recovery path: error -> aborted."""
        state_machine.transition(WorkflowState.PRE_PROCEDURE)
        state_machine.transition(WorkflowState.PATIENT_ON_TABLE)
        state_machine.transition(WorkflowState.PROCEDURE_ACTIVE)
        state_machine.transition(WorkflowState.ERROR)
        state_machine.transition(WorkflowState.ABORTED)
        assert state_machine.current_state == WorkflowState.ABORTED


class TestInvalidTransitions:
    """TC-007.2, TC-RM-001.1: Verify invalid transitions are rejected."""

    def test_cannot_skip_states(self, state_machine):
        """Cannot jump from created directly to procedure_active."""
        assert not state_machine.can_transition(WorkflowState.PROCEDURE_ACTIVE)
        with pytest.raises(ValueError, match="Invalid transition"):
            state_machine.transition(WorkflowState.PROCEDURE_ACTIVE)

    def test_cannot_go_backwards(self, state_machine):
        """Cannot transition backwards in the flow."""
        state_machine.transition(WorkflowState.PRE_PROCEDURE)
        state_machine.transition(WorkflowState.PATIENT_ON_TABLE)
        assert not state_machine.can_transition(WorkflowState.PRE_PROCEDURE)

    def test_completed_is_terminal(self, state_machine):
        """Completed state allows no further transitions."""
        for state in [
            WorkflowState.PRE_PROCEDURE,
            WorkflowState.PATIENT_ON_TABLE,
            WorkflowState.PROCEDURE_ACTIVE,
            WorkflowState.POST_PROCEDURE,
            WorkflowState.COMPLETED,
        ]:
            state_machine.transition(state)
        assert state_machine.is_terminal()
        assert state_machine.allowed_transitions() == []


class TestEmergencyAbort:
    """TC-007.4: Emergency abort available from all active states."""

    @pytest.mark.parametrize(
        "states_before_abort",
        [
            [],  # abort from created
            [WorkflowState.PRE_PROCEDURE],
            [WorkflowState.PRE_PROCEDURE, WorkflowState.PATIENT_ON_TABLE],
            [
                WorkflowState.PRE_PROCEDURE,
                WorkflowState.PATIENT_ON_TABLE,
                WorkflowState.PROCEDURE_ACTIVE,
            ],
        ],
    )
    def test_abort_from_active_states(self, states_before_abort):
        """Abort is reachable from created, pre_procedure, patient_on_table, procedure_active."""
        sm = StateMachine()
        for state in states_before_abort:
            sm.transition(state)
        assert sm.can_transition(WorkflowState.ABORTED)
        sm.transition(WorkflowState.ABORTED)
        assert sm.current_state == WorkflowState.ABORTED
        assert sm.is_terminal()


class TestTransitionGraph:
    """TC-007.3: Verify transition graph integrity."""

    def test_all_states_have_transitions_defined(self):
        """Every WorkflowState must appear in TRANSITIONS dict."""
        for state in WorkflowState:
            assert state in TRANSITIONS, f"Missing transitions for {state}"

    def test_terminal_states_have_no_outgoing(self):
        """Terminal states (completed, aborted) must have empty transition sets."""
        assert TRANSITIONS[WorkflowState.COMPLETED] == set()
        assert TRANSITIONS[WorkflowState.ABORTED] == set()
