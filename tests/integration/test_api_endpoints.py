"""
Integration tests for API endpoints.

Verifies end-to-end behavior through the FastAPI application,
including middleware (audit logging) and routing.

Traceability:
  - TC-001.1: Root endpoint returns service info (REQ-001)
  - TC-003.1: Health endpoints return expected structure (REQ-003)
  - TC-006.3: Workflow E2E via API (REQ-006)
"""

import pytest
from fastapi.testclient import TestClient
from src.azurioneye_operator.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestRootEndpoint:
    """TC-001.1: Service info endpoint."""

    def test_root_returns_service_info(self, client):
        """REQ-001: Root endpoint identifies the service."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "AzurionEye AI Operator"
        assert "version" in data
        assert data["safety_class"] == "IEC 62304 Class B"


class TestHealthEndpoints:
    """TC-003.1: Health check endpoints."""

    def test_liveness_probe(self, client):
        """REQ-003: Liveness returns alive status."""
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_readiness_probe(self, client):
        """REQ-003: Readiness returns check results."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert "checks" in data
        assert "model_loaded" in data["checks"]


class TestWorkflowE2E:
    """TC-006.3: End-to-end workflow via API."""

    def test_create_and_transition_workflow(self, client):
        """REQ-006: Create workflow and advance through states."""
        # Create
        response = client.post(
            "/orchestrate/start",
            json={
                "procedure_type": "pci",
                "patient_id": "TEST-001",
                "operator_id": "DR-TEST",
                "lab_id": "cath-lab-01",
            },
        )
        assert response.status_code == 200
        wf = response.json()
        wf_id = wf["id"]
        assert wf["state"] == "created"

        # Transition to pre_procedure
        response = client.post(
            "/orchestrate/transition",
            json={"workflow_id": wf_id, "target_state": "pre_procedure"},
        )
        assert response.status_code == 200
        assert response.json()["state"] == "pre_procedure"

        # Get status
        response = client.get(f"/orchestrate/status/{wf_id}")
        assert response.status_code == 200
        assert response.json()["state"] == "pre_procedure"

    def test_invalid_transition_returns_400(self, client):
        """REQ-007, RM-001: Invalid transition is rejected with 400."""
        # Create workflow
        response = client.post(
            "/orchestrate/start",
            json={
                "procedure_type": "pci",
                "patient_id": "TEST-002",
                "operator_id": "DR-TEST",
            },
        )
        wf_id = response.json()["id"]

        # Try invalid skip
        response = client.post(
            "/orchestrate/transition",
            json={"workflow_id": wf_id, "target_state": "completed"},
        )
        assert response.status_code == 400
