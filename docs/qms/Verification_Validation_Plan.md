# Verification & Validation Plan
## IEC 62304 Sections 5.5, 5.6, 5.7

**Document ID**: VVP-001
**Version**: 0.1.0
**Safety Classification**: Class B

---

## 1. Verification Strategy

### 1.1 Unit Verification (IEC 62304 5.5)

| Aspect | Approach |
|--------|----------|
| Framework | pytest |
| Location | `tests/unit/` |
| Coverage Target | >= 80% (Class B minimum) |
| Evidence | JUnit XML + coverage.xml (auto-ingested by Ketryx) |
| Naming Convention | `test_{module}.py` with TC-XXX references in docstrings |

### 1.2 Integration Testing (IEC 62304 5.6)

| Aspect | Approach |
|--------|----------|
| Framework | pytest + FastAPI TestClient |
| Location | `tests/integration/` |
| Scope | API endpoint contracts, workflow E2E, data persistence |
| Evidence | JUnit XML (auto-ingested by Ketryx) |

### 1.3 System Testing (IEC 62304 5.7)

| Aspect | Approach |
|--------|----------|
| Type | Manual + automated |
| Scope | Full workflow from clinical event to audit log |
| Environment | Docker containerized, production-like |
| Evidence | Test execution records in Ketryx |

## 2. Test-to-Requirement Mapping

Every test case references the requirement(s) it verifies:
- In test docstrings: `Verifies: REQ-007`
- In GitHub Issues: Test Case issue linked to Requirement issue
- In Ketryx: Auto-linked via label and ID pattern matching

## 3. Validation Approach

Validation confirms the device meets user needs (not just requirements):
- Clinical workflow validation with representative procedure scenarios
- User acceptance testing with interventional cardiologists
- Performance validation under realistic cath lab conditions

## 4. Test Environment

| Environment | Purpose |
|---|---|
| Local (pytest) | Developer unit/integration testing |
| CI (GitHub Actions) | Automated verification on every PR |
| Staging (Docker Compose) | System testing, pre-release validation |
| Ketryx Sandbox | Compliance evidence aggregation and review |

## 5. Pass/Fail Criteria

A release is PASS if:
- All unit tests pass (0 failures)
- All integration tests pass (0 failures)
- Code coverage >= 80%
- No HIGH/CRITICAL security findings
- All requirements have linked, passing test cases
- All HIGH risk mitigations are verified
- Ketryx release gates all GREEN
