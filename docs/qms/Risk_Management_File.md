# Risk Management File
## ISO 14971 Integration

**Document ID**: RMF-001
**Version**: 0.1.0
**Safety Classification**: Class B
**Ketryx Sync**: Risk items are managed as GitHub Issues (label: `type/risk-item`) and auto-synced to Ketryx. Test pass/fail auto-updates risk verification status.

---

## 1. Risk Management Process

Risk management follows ISO 14971:2019. Risks are identified, analyzed, evaluated, and controlled through the software development lifecycle. Ketryx provides real-time tracking of risk mitigation verification.

## 2. Risk Acceptability Matrix

| Probability / Severity | Negligible | Minor | Serious | Critical | Catastrophic |
|---|---|---|---|---|---|
| Frequent | MEDIUM | HIGH | HIGH | HIGH | HIGH |
| Probable | LOW | MEDIUM | HIGH | HIGH | HIGH |
| Occasional | LOW | LOW | MEDIUM | HIGH | HIGH |
| Remote | LOW | LOW | LOW | MEDIUM | HIGH |
| Improbable | LOW | LOW | LOW | LOW | MEDIUM |

## 3. Identified Risks

### RM-001: Invalid Clinical State Transition
- **Hazard**: Workflow engine allows clinically inappropriate state transition
- **Hazardous Situation**: Cath lab procedure proceeds with incorrect workflow state
- **Harm**: Incorrect clinical application displayed, potential for delayed treatment
- **Severity**: Serious | **Probability**: Remote | **Risk Level**: LOW (post-mitigation)
- **Mitigation**: State machine validation (REQ-007) with explicit transition graph. All transitions validated before execution. Invalid transitions logged to audit trail.
- **Verification**: TC-007.1, TC-007.2, TC-007.3, TC-007.4, TC-RM-001.1
- **Ketryx Status**: Verified (all linked tests PASS)

### RM-002: Lost Workflow Context
- **Hazard**: Workflow state or history lost during operation
- **Hazardous Situation**: Clinical team loses visibility into procedure progress
- **Harm**: Delayed clinical decisions, repeated manual steps
- **Severity**: Minor | **Probability**: Occasional | **Risk Level**: LOW
- **Mitigation**: Persistent state storage + audit log (REQ-002). All state changes logged with full context.
- **Verification**: TC-006.1, TC-006.2, TC-008.1
- **Ketryx Status**: Verified

### RM-003: Incorrect Cardiac Rhythm Classification
- **Hazard**: ML model returns wrong classification
- **Hazardous Situation**: Clinician acts on incorrect rhythm assessment
- **Harm**: Inappropriate treatment decision
- **Severity**: Critical | **Probability**: Occasional | **Risk Level**: HIGH (pre-mitigation), MEDIUM (post)
- **Mitigation**: Confidence threshold (0.85). Below threshold, "requires_human_review" flag is set (REQ-010). Classification is advisory only, never autonomous.
- **Verification**: TC-009.1, TC-010.1, TC-RM-003.1
- **Ketryx Status**: Verified

### RM-004: Performance Degradation
- **Hazard**: Inference or API latency exceeds 500ms threshold
- **Hazardous Situation**: Clinical workflow stalls, procedure delayed
- **Harm**: Procedure time increased, patient under anesthesia longer
- **Severity**: Minor | **Probability**: Occasional | **Risk Level**: LOW
- **Mitigation**: Latency monitoring with alerting (REQ-005, REQ-012). Self-reported inference time in every response.
- **Verification**: TC-012.1
- **Ketryx Status**: Verified

### RM-005: Data Validation Bypass
- **Hazard**: Malformed clinical data processed without validation
- **Hazardous Situation**: System operates on corrupt/invalid input
- **Harm**: Incorrect workflow state or classification
- **Severity**: Serious | **Probability**: Remote | **Risk Level**: LOW
- **Mitigation**: Strict Pydantic validation on all API inputs (REQ-011). Signal quality assessment before inference.
- **Verification**: TC-011.1, TC-011.2
- **Ketryx Status**: Verified

### RM-006: Service Unavailability
- **Hazard**: AI Operator service crashes or becomes unresponsive
- **Hazardous Situation**: Cath lab loses AI-assisted workflow
- **Harm**: Manual fallback required, efficiency loss
- **Severity**: Minor | **Probability**: Remote | **Risk Level**: LOW
- **Mitigation**: Health check endpoints (REQ-003) for Kubernetes liveness/readiness probes. Graceful degradation to manual operation.
- **Verification**: Health endpoint tests
- **Ketryx Status**: Verified

## 4. Residual Risk Summary

| Risk ID | Pre-Mitigation | Post-Mitigation | Acceptable? |
|---------|---------------|-----------------|-------------|
| RM-001 | MEDIUM | LOW | Yes |
| RM-002 | LOW | LOW | Yes |
| RM-003 | HIGH | MEDIUM | Yes (ALARP, human-in-the-loop) |
| RM-004 | LOW | LOW | Yes |
| RM-005 | MEDIUM | LOW | Yes |
| RM-006 | LOW | LOW | Yes |

## 5. Overall Residual Risk

The overall residual risk of the AzurionEye AI Operator is **ACCEPTABLE**. The highest residual risk (RM-003, MEDIUM) is managed through human-in-the-loop design: the system is advisory only, all low-confidence predictions are flagged, and the clinician retains full decision authority.
