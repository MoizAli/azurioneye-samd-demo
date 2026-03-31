# Software Architecture Design Document (SADD)
## IEC 62304 Section 5.3

**Document ID**: SADD-001
**Version**: 0.1.0

---

## 1. System Context

The AzurionEye AI Operator is a FastAPI-based microservice that runs on the AI Companion PC (HP Z2 G1i) in the cath lab. It receives clinical events from the Azurion system, orchestrates workflow state transitions, and provides ML-based cardiac rhythm classification.

```
                    +------------------+
                    |   Azurion System  |
                    |  (X-ray + Events) |
                    +--------+---------+
                             |
                     Clinical Events
                             |
                    +--------v---------+
                    | AzurionEye       |
                    | AI Operator      |
                    | (This Service)   |
                    +--+-----+-----+--+
                       |     |     |
              +--------+  +--+--+  +--------+
              |           |     |           |
        Audit Log    ML Model   Event Bus
        (PostgreSQL) (PyTorch)  (Downstream)
```

## 2. Container Architecture

| Container | Technology | Responsibility |
|-----------|-----------|---------------|
| API Gateway | FastAPI | Request routing, validation, audit logging |
| Orchestration Engine | Python | Workflow state machine, transition validation |
| Inference Pipeline | PyTorch | Cardiac rhythm classification |
| Audit Logger | Structured JSON | Immutable clinical decision log |
| Health Monitor | FastAPI endpoints | Liveness/readiness for Kubernetes |

## 3. Component Design

### 3.1 API Layer (`src/azurioneye_operator/api/`)
- `health.py`: Liveness and readiness probes
- `orchestrate.py`: Workflow CRUD + state transitions
- `predict.py`: ML inference endpoint

### 3.2 Core Layer (`src/azurioneye_operator/core/`)
- `orchestrator.py`: Workflow lifecycle management
- `state_manager.py`: State machine with transition validation

### 3.3 Infrastructure Layer (`src/azurioneye_operator/infra/`)
- `audit_logger.py`: Structured audit logging

## 4. Key Design Decisions

| Decision | Rationale | IEC 62304 Impact |
|----------|-----------|-----------------|
| State machine for workflow | Prevents invalid clinical states (RM-001) | Verifiable transition graph |
| Confidence threshold for ML | Human-in-the-loop for low confidence (RM-003) | Safety mitigation evidence |
| Audit middleware | Every request logged automatically (REQ-002) | Compliance evidence |
| Pydantic validation | Schema-enforced input validation (REQ-011) | Safety boundary |

## 5. External Interfaces

| Interface | Protocol | Direction | Design Input |
|-----------|----------|-----------|-------------|
| Azurion Events | FHIR / REST | Inbound | D-014 (FHIR for external, events for internal) |
| Downstream Consumers | Event Bus | Outbound | REQ-008 |
| Audit Storage | PostgreSQL | Outbound | REQ-002 |
| ML Model Registry | File System / ClearML | Internal | REQ-004 |
