"""
Pytest fixtures and configuration for AzurionEye test suite.

Test organization maps to IEC 62304 verification levels:
  - unit/    -> Software unit verification (Section 5.5)
  - integration/ -> Software integration testing (Section 5.6)
  - compliance/  -> Compliance evidence verification
"""

import pytest
from fastapi.testclient import TestClient

from src.azurioneye_operator.main import app
from src.azurioneye_operator.core.state_manager import StateMachine, WorkflowState


@pytest.fixture
def client():
    """FastAPI test client for API testing."""
    return TestClient(app)


@pytest.fixture
def state_machine():
    """Fresh state machine instance for unit tests."""
    return StateMachine()


@pytest.fixture
def sample_ecg_signal():
    """
    Sample ECG signal data for inference tests.
    Simulates 1 second of Lead II data at 250Hz.
    """
    import math
    # Generate a simplified QRS-like waveform
    signal = []
    for i in range(250):
        t = i / 250.0
        # P wave + QRS complex + T wave (simplified)
        p_wave = 0.1 * math.sin(2 * math.pi * 1.2 * t)
        qrs = 1.0 * math.exp(-((t % 0.8 - 0.2) ** 2) / 0.002)
        t_wave = 0.3 * math.sin(2 * math.pi * 0.8 * (t - 0.3))
        signal.append(p_wave + qrs + t_wave)
    return signal


@pytest.fixture
def noise_signal():
    """Noisy signal that should fail quality check."""
    import random
    random.seed(42)
    return [random.gauss(0, 50) for _ in range(250)]


@pytest.fixture
def workflow_start_payload():
    """Standard workflow start request payload."""
    return {
        "procedure_type": "pci",
        "patient_id": "PATIENT-001",
        "operator_id": "DR-SMITH",
        "lab_id": "cath-lab-01",
    }
