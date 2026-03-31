# Software Requirements Specification (SRS)
## IEC 62304 Section 5.2

**Document ID**: SRS-001
**Version**: 0.1.0
**Safety Classification**: Class B
**Ketryx Sync**: Requirements are managed as GitHub Issues (label: `type/requirement`) and auto-synced to Ketryx traceability matrix.

---

## 1. User Needs

| ID | User Need | Source |
|----|-----------|--------|
| UN-001 | Cardiologists need automated clinical workflow orchestration during cath lab procedures | Stakeholder interviews |
| UN-002 | Clinical staff need all decisions logged for audit and quality review | Regulatory (IEC 62304) |
| UN-003 | IT operations need to monitor service health in real-time | Operational requirement |
| UN-004 | Cardiologists need AI-assisted cardiac rhythm classification | Clinical workflow analysis |
| UN-005 | Risk management requires confidence thresholds for AI predictions | ISO 14971 |

## 2. Software Requirements

### 2.1 Functional Requirements

| ID | Requirement | Source | Priority | Safety-Critical |
|----|------------|--------|----------|----------------|
| REQ-001 | System shall provide REST API for clinical workflow orchestration | UN-001 | Must | No |
| REQ-002 | System shall maintain audit log of all clinical decisions with timestamp | UN-002 | Must | Yes |
| REQ-003 | System shall expose health check endpoints (liveness + readiness) | UN-003 | Must | No |
| REQ-004 | System shall load and verify ML model version on startup | UN-004 | Must | Yes |
| REQ-005 | System shall process all requests within 500ms latency | UN-001 | Must | Yes |
| REQ-006 | System shall manage clinical workflow lifecycle (create, transition, complete) | UN-001 | Must | No |
| REQ-007 | System shall validate all state transitions against allowed transition graph | UN-001 | Must | Yes |
| REQ-008 | System shall emit events on workflow state transitions | UN-001 | Should | No |
| REQ-009 | System shall classify cardiac rhythm from ECG signal input | UN-004 | Must | Yes |
| REQ-010 | System shall return classification with confidence score | UN-004, UN-005 | Must | Yes |
| REQ-011 | System shall reject inputs that fail validation (signal length, lead name, quality) | UN-005 | Must | Yes |
| REQ-012 | ML inference latency shall be <500ms | UN-001 | Must | Yes |

### 2.2 Non-Functional Requirements

| ID | Requirement | Category |
|----|------------|----------|
| NFR-001 | Code coverage shall be >= 80% for all releases | Quality |
| NFR-002 | All dependencies shall be declared in SBOM (CycloneDX format) | Compliance |
| NFR-003 | No HIGH/CRITICAL CVEs in production dependencies | Security |
| NFR-004 | All API endpoints shall validate input against Pydantic schemas | Security |
| NFR-005 | Audit logs shall be immutable and retained for device lifetime | Compliance |

## 3. Traceability

Full traceability is maintained via Ketryx:
- User Need -> Requirement: Documented in "Source" column above
- Requirement -> Design: Implemented in code with REQ-XXX references in docstrings
- Requirement -> Test: Linked via GitHub Issues and test file naming (TC-XXX)
- Requirement -> Risk: Cross-referenced in Risk Management File

See `.ketryx/config.yaml` for auto-linking rules.
