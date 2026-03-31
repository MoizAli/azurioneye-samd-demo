"""
Unit tests for workflow orchestrator.

Verifies:
  - REQ-006: Workflow lifecycle management
  - REQ-008: Event emission on state changes

Traceability:
  - TC-006.1: Workflow creation returns valid structure
  - TC-006.2: Workflow status retrieval
  - TC-008.1: State transitions update history
"""

import pytest
from src.azurioneye_operator.core.orchestrator import WorkflowOrchestrator


@pytest.fixture
def orchestrator():
    return WorkflowOrchestrator()


class TestWorkflowCreation:
    """TC-006.1: Workflow creation."""

    def test_create_workflow_returns_id(self, orchestrator):
        """REQ-006: Created workflow has a unique ID."""
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        assert wf["id"].startswith("WF-")
        assert len(wf["id"]) == 11  # WF- + 8 hex chars

    def test_create_workflow_initial_state(self, orchestrator):
        """REQ-006: New workflow starts in 'created' state."""
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        assert wf["state"] == "created"

    def test_create_workflow_has_history(self, orchestrator):
        """REQ-008: Workflow history starts with creation event."""
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        assert len(wf["history"]) == 1
        assert wf["history"][0]["action"] == "created"


class TestWorkflowTransitions:
    """TC-008.1: State transitions update history."""

    def test_transition_updates_state(self, orchestrator):
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        result = orchestrator.transition(wf["id"], "pre_procedure")
        assert result["state"] == "pre_procedure"

    def test_transition_appends_to_history(self, orchestrator):
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        orchestrator.transition(wf["id"], "pre_procedure")
        result = orchestrator.transition(wf["id"], "patient_on_table")
        assert len(result["history"]) == 3

    def test_invalid_workflow_id_raises(self, orchestrator):
        with pytest.raises(ValueError, match="not found"):
            orchestrator.transition("WF-NONEXIST", "pre_procedure")

    def test_invalid_target_state_raises(self, orchestrator):
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        with pytest.raises(ValueError, match="Invalid state"):
            orchestrator.transition(wf["id"], "nonsense_state")


class TestWorkflowStatus:
    """TC-006.2: Workflow status retrieval."""

    def test_get_existing_workflow(self, orchestrator):
        wf = orchestrator.create_workflow(
            procedure_type="pci",
            patient_id="P-001",
            operator_id="DR-001",
            lab_id="lab-01",
        )
        status = orchestrator.get_status(wf["id"])
        assert status is not None
        assert status["id"] == wf["id"]

    def test_get_nonexistent_workflow(self, orchestrator):
        status = orchestrator.get_status("WF-NONEXIST")
        assert status is None
