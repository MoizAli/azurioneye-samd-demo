# Traceability Matrix
## Requirements -> Design -> Code -> Tests -> Risks

**Note**: This is a snapshot. The live traceability matrix is auto-maintained by Ketryx from GitHub Issues and CI test results.

---

## Full Traceability

| User Need | Requirement | Design Element | Code Location | Test Case(s) | Risk Item(s) |
|-----------|------------|----------------|---------------|-------------|-------------|
| UN-001 | REQ-001 | SADD 3.1 API Layer | `api/orchestrate.py` | TC-006.1 | - |
| UN-002 | REQ-002 | SADD 3.3 Infra | `infra/audit_logger.py`, middleware in `main.py` | TC-002.1 | RM-002 |
| UN-003 | REQ-003 | SADD 3.1 API Layer | `api/health.py` | TC-003.1 | RM-006 |
| UN-004 | REQ-004 | SADD 3.2 Core | `main.py` (lifespan) | TC-004.1 | - |
| UN-001 | REQ-005 | SADD 4 (NFR) | middleware in `main.py` | TC-012.1 | RM-004 |
| UN-001 | REQ-006 | SADD 3.2 Core | `core/orchestrator.py` | TC-006.1, TC-006.2, TC-008.1 | - |
| UN-001 | REQ-007 | SADD 3.2 Core | `core/state_manager.py` | TC-007.1, TC-007.2, TC-007.3, TC-007.4, TC-RM-001.1 | RM-001 |
| UN-001 | REQ-008 | SADD 3.2 Core | `core/orchestrator.py` | TC-008.1 | - |
| UN-004 | REQ-009 | SADD 4.2 Inference | `api/predict.py` | TC-009.1 | RM-003 |
| UN-004, UN-005 | REQ-010 | SADD 4.2 Inference | `api/predict.py` | TC-010.1, TC-RM-003.1 | RM-003 |
| UN-005 | REQ-011 | SADD 4.2 Inference | `api/predict.py` | TC-011.1, TC-011.2 | RM-005 |
| UN-001 | REQ-012 | SADD 4.2 Inference | `api/predict.py` | TC-012.1 | RM-004 |

## Coverage Summary

| Category | Total | Covered | Gap |
|----------|-------|---------|-----|
| Requirements with tests | 12 | 12 | 0 |
| Requirements with code | 12 | 12 | 0 |
| Risk items with verification | 6 | 6 | 0 |
| User needs with requirements | 5 | 5 | 0 |

**Ketryx auto-generates this matrix from GitHub data. Gaps are flagged in real-time.**
