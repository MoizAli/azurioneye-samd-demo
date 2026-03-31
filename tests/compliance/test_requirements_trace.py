"""
Compliance tests: verify that traceability is maintained in the codebase.

These tests are meta-tests that verify the engineering discipline of
maintaining requirement references in code and test files.

Traceability:
  - NFR-001: Code coverage >= 80%
  - NFR-002: All dependencies declared
"""

import os
import re
import pytest


# Paths relative to project root
SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "src")
TEST_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "requirements.txt")


class TestRequirementTraceability:
    """Verify that code references requirements properly."""

    def test_source_files_reference_requirements(self):
        """Every API module should reference at least one REQ-XXX."""
        api_dir = os.path.join(SRC_DIR, "azurioneye_operator", "api")
        if not os.path.exists(api_dir):
            pytest.skip("Source directory not found")

        for filename in os.listdir(api_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                filepath = os.path.join(api_dir, filename)
                with open(filepath) as f:
                    content = f.read()
                req_refs = re.findall(r"REQ-\d+", content)
                assert len(req_refs) > 0, (
                    f"{filename} has no REQ-XXX references in docstrings"
                )

    def test_test_files_reference_test_cases(self):
        """Every test module should reference at least one TC-XXX."""
        unit_dir = os.path.join(TEST_DIR, "tests", "unit")
        if not os.path.exists(unit_dir):
            pytest.skip("Test directory not found")

        for filename in os.listdir(unit_dir):
            if filename.startswith("test_") and filename.endswith(".py"):
                filepath = os.path.join(unit_dir, filename)
                with open(filepath) as f:
                    content = f.read()
                tc_refs = re.findall(r"TC-[\w.-]+", content)
                assert len(tc_refs) > 0, (
                    f"{filename} has no TC-XXX references"
                )


class TestDependencyDeclaration:
    """NFR-002: All dependencies must be declared."""

    def test_requirements_file_exists(self):
        """requirements.txt must exist for SBOM generation."""
        assert os.path.exists(REQUIREMENTS_FILE), "requirements.txt not found"

    def test_requirements_are_pinned(self):
        """All production dependencies must have pinned versions."""
        if not os.path.exists(REQUIREMENTS_FILE):
            pytest.skip("requirements.txt not found")

        with open(REQUIREMENTS_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    assert "==" in line, (
                        f"Dependency not pinned: {line}. "
                        f"Use == for reproducible builds."
                    )
