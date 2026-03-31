# Software Development Plan (SDP)
## IEC 62304 Section 5.1

**Document ID**: SDP-001
**Version**: 0.1.0
**Safety Classification**: Class B
**Product**: AzurionEye AI Operator + Orchestrator
**Regulatory Pathway**: FDA 510(k) with PCCP

---

## 1. Purpose

This Software Development Plan defines the lifecycle processes, tools, roles, and deliverables for the AzurionEye AI Operator, a Software as Medical Device (SaMD) classified as IEC 62304 Class B.

## 2. Scope

The AI Operator provides:
- Clinical workflow orchestration for interventional cardiology (cath lab)
- Cardiac rhythm classification via ML inference
- Audit trail for all clinical decisions
- Event-driven architecture for downstream consumer integration

## 3. Software Safety Classification

**Class B** (IEC 62304): Software system where failure could result in non-serious injury. This classification drives the following minimum requirements:
- Software requirements analysis (Section 5.2)
- Software architectural design (Section 5.3)
- Software unit verification (Section 5.5)
- Software integration and integration testing (Section 5.6)
- Software system testing (Section 5.7)
- Software release (Section 5.8)

## 4. Development Lifecycle Model

Agile with regulatory gates. Two-week sprints with the following compliance checkpoints:

| Sprint Phase | Compliance Activity |
|---|---|
| Sprint Planning | Requirements review, risk assessment update |
| Development | Traceability maintained via GitHub issue linking |
| Sprint Review | Design review via PR checklist |
| Release (per milestone) | 7-gate compliance check via Ketryx |

## 5. Tools

| Purpose | Tool | Integration |
|---------|------|-------------|
| Source Control | GitHub | Ketryx bidirectional sync |
| CI/CD | GitHub Actions | Test results -> Ketryx verification |
| Issue Tracking | GitHub Issues | Requirements/risks -> Ketryx traceability |
| Compliance Orchestration | Ketryx | Auto-traceability, release gates, document generation |
| Static Analysis | Ruff, Bandit | CI pipeline |
| Test Framework | pytest | JUnit XML -> Ketryx ingestion |
| SBOM | CycloneDX | Auto-generated on release -> Ketryx SOUP |
| Containerization | Docker | Reproducible builds |

## 6. Roles and Responsibilities

| Role | Responsibility |
|------|---------------|
| Software Developer | Implement requirements, write tests, maintain traceability |
| Software Architect | Design review, architecture decisions |
| QMS Lead | QMS artifact review, compliance verification |
| Regulatory Affairs | 510(k) submission, intended use validation |
| Risk Manager | ISO 14971 risk management file maintenance |
| Release Manager | Release gate verification, SOUP review |

## 7. Configuration Management

- All source code versioned in Git (GitHub)
- Semantic versioning (MAJOR.MINOR.PATCH)
- Branch protection: main requires PR + 2 approvals + passing CI
- Every release tagged and associated with SBOM + compliance bundle

## 8. Deliverables

| IEC 62304 Section | Deliverable | Location |
|---|---|---|
| 5.1 | Software Development Plan | This document |
| 5.2 | Software Requirements Specification | `docs/qms/Software_Requirements_Specification.md` + GitHub Issues |
| 5.3 | Software Architecture Design | `docs/qms/Software_Architecture_Design.md` |
| 5.4 | Software Detailed Design | Code docstrings + `docs/architecture/` |
| 5.5 | Unit Verification Results | CI artifacts (JUnit XML) |
| 5.6 | Integration Test Results | CI artifacts (JUnit XML) |
| 5.7 | System Test Results | Manual + automated |
| 5.8 | Release Package | GitHub Release + Ketryx compliance bundle |
| ISO 14971 | Risk Management File | `docs/qms/Risk_Management_File.md` + GitHub Issues |
