#!/bin/bash
# =============================================================================
# AzurionEye SaMD Demo - GitHub Setup Script
# Run this from the azurioneye-samd-demo/ directory on your local machine
#
# Prerequisites:
#   - gh CLI installed (brew install gh)
#   - gh auth login (already authenticated)
#   - git installed
#
# What this script does:
#   1. Pushes all code to github.com/MoizAli/azurioneye-samd-demo
#   2. Creates labels for Ketryx traceability
#   3. Creates GitHub Issues (REQ, RM, TC) with proper labels and links
#   4. Triggers CI by pushing a tag
# =============================================================================

set -e
REPO="MoizAli/azurioneye-samd-demo"

echo "=== Step 1: Push code to GitHub ==="
git init -b main 2>/dev/null || true
git add -A
git commit -m "Initial commit: AzurionEye SaMD demo repo for Ketryx evaluation

Complete IEC 62304 Class B repository with:
- FastAPI service (orchestration + ML inference)
- 37 passing tests (unit, integration, compliance)
- 7 QMS documents (SDP, SRS, SADD, V&V, RMF, SOUP, Traceability)
- 4 GitHub Actions workflows (CI, security, SBOM, release)
- Ketryx config with 7-gate release checklist
- GitHub issue/PR templates for regulatory traceability" 2>/dev/null || echo "Already committed"

git remote add origin "https://github.com/${REPO}.git" 2>/dev/null || git remote set-url origin "https://github.com/${REPO}.git"
git push -u origin main --force

echo ""
echo "=== Step 2: Create labels ==="
# Requirement types
gh label create "type/requirement" --color "0075ca" --description "Software requirement (SRS item)" --repo "$REPO" 2>/dev/null || true
gh label create "type/risk-item" --color "d73a4a" --description "ISO 14971 risk item" --repo "$REPO" 2>/dev/null || true
gh label create "type/test-case" --color "2ea44f" --description "Verification test case" --repo "$REPO" 2>/dev/null || true
gh label create "type/problem-report" --color "e4e669" --description "IEC 62304 problem report" --repo "$REPO" 2>/dev/null || true
gh label create "type/user-need" --color "7057ff" --description "User need (SRS input)" --repo "$REPO" 2>/dev/null || true
gh label create "type/design-input" --color "bfd4f2" --description "Design input" --repo "$REPO" 2>/dev/null || true

# Safety classes
gh label create "safety-class/A" --color "c5def5" --description "IEC 62304 Class A" --repo "$REPO" 2>/dev/null || true
gh label create "safety-class/B" --color "fbca04" --description "IEC 62304 Class B" --repo "$REPO" 2>/dev/null || true
gh label create "safety-class/C" --color "d93f0b" --description "IEC 62304 Class C" --repo "$REPO" 2>/dev/null || true

# Risk levels
gh label create "risk-level/high" --color "d73a4a" --description "High risk (unacceptable pre-mitigation)" --repo "$REPO" 2>/dev/null || true
gh label create "risk-level/medium" --color "fbca04" --description "Medium risk (ALARP required)" --repo "$REPO" 2>/dev/null || true
gh label create "risk-level/low" --color "0e8a16" --description "Low risk (acceptable)" --repo "$REPO" 2>/dev/null || true

# Verification status
gh label create "verification-status/pending" --color "e4e669" --description "Test not yet executed" --repo "$REPO" 2>/dev/null || true
gh label create "verification-status/passed" --color "0e8a16" --description "Test passed" --repo "$REPO" 2>/dev/null || true
gh label create "verification-status/failed" --color "d73a4a" --description "Test failed" --repo "$REPO" 2>/dev/null || true

# Safety critical
gh label create "safety-critical" --color "b60205" --description "Affects patient safety" --repo "$REPO" 2>/dev/null || true

echo ""
echo "=== Step 3: Create User Need Issues ==="

gh issue create --repo "$REPO" \
  --title "[UN-001] Automated clinical workflow orchestration during cath lab procedures" \
  --label "type/user-need" \
  --body "**User Need ID**: UN-001
**Source**: Stakeholder interviews

Cardiologists need automated clinical workflow orchestration during cath lab procedures to reduce manual steps and improve procedural efficiency.

**Derived Requirements**: REQ-001, REQ-005, REQ-006, REQ-007, REQ-008, REQ-012"

gh issue create --repo "$REPO" \
  --title "[UN-002] All clinical decisions logged for audit and quality review" \
  --label "type/user-need" \
  --body "**User Need ID**: UN-002
**Source**: Regulatory (IEC 62304)

Clinical staff need all decisions logged for audit and quality review to meet regulatory requirements.

**Derived Requirements**: REQ-002"

gh issue create --repo "$REPO" \
  --title "[UN-003] Real-time service health monitoring" \
  --label "type/user-need" \
  --body "**User Need ID**: UN-003
**Source**: Operational requirement

IT operations need to monitor service health in real-time.

**Derived Requirements**: REQ-003"

gh issue create --repo "$REPO" \
  --title "[UN-004] AI-assisted cardiac rhythm classification" \
  --label "type/user-need" \
  --body "**User Need ID**: UN-004
**Source**: Clinical workflow analysis

Cardiologists need AI-assisted cardiac rhythm classification during procedures.

**Derived Requirements**: REQ-004, REQ-009, REQ-010"

gh issue create --repo "$REPO" \
  --title "[UN-005] Confidence thresholds for AI predictions" \
  --label "type/user-need" \
  --body "**User Need ID**: UN-005
**Source**: ISO 14971 / Risk Management

Risk management requires confidence thresholds for AI predictions to ensure human review when confidence is low.

**Derived Requirements**: REQ-010, REQ-011"

echo ""
echo "=== Step 4: Create Requirement Issues ==="

gh issue create --repo "$REPO" \
  --title "[REQ-001] System shall provide REST API for clinical workflow orchestration" \
  --label "type/requirement,safety-class/B" \
  --body "**Requirement ID**: REQ-001
**Source**: UN-001
**Safety-Critical**: No
**Priority**: Must

The system shall provide a REST API for clinical workflow orchestration.

**Acceptance Criteria**:
1. POST /orchestrate/start creates a new workflow
2. POST /orchestrate/transition transitions workflow state
3. GET /orchestrate/status/{id} returns current state

**Verification Method**: Integration Test
**Test Case(s)**: TC-001.1, TC-006.3
**Code Location**: \`src/azurioneye_operator/api/orchestrate.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-002] System shall maintain audit log of all clinical decisions" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-002
**Source**: UN-002
**Safety-Critical**: Yes
**Priority**: Must

The system shall maintain an audit log of all clinical decisions with timestamp.

**Acceptance Criteria**:
1. Every API request logged with timestamp, method, path, status
2. Clinical decisions include clinical_decision=true flag
3. Logs are structured JSON for machine parsing

**Verification Method**: Unit Test + Integration Test
**Risk Item(s)**: RM-002
**Code Location**: \`src/azurioneye_operator/infra/audit_logger.py\`, middleware in \`main.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-003] System shall expose health check endpoints" \
  --label "type/requirement,safety-class/B" \
  --body "**Requirement ID**: REQ-003
**Source**: UN-003
**Safety-Critical**: No

The system shall expose health check endpoints (liveness + readiness) for operational monitoring.

**Verification Method**: Integration Test
**Test Case(s)**: TC-003.1
**Risk Item(s)**: RM-006
**Code Location**: \`src/azurioneye_operator/api/health.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-004] System shall load and verify ML model version on startup" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-004
**Source**: UN-004
**Safety-Critical**: Yes

The system shall load and verify ML model version on startup.

**Verification Method**: Unit Test
**Code Location**: \`src/azurioneye_operator/main.py\` (lifespan)"

gh issue create --repo "$REPO" \
  --title "[REQ-005] System shall process all requests within 500ms latency" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-005
**Source**: UN-001
**Safety-Critical**: Yes

The system shall process all requests within 500ms latency.

**Verification Method**: Performance Test
**Test Case(s)**: TC-012.1
**Risk Item(s)**: RM-004
**Code Location**: middleware in \`main.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-006] System shall manage clinical workflow lifecycle" \
  --label "type/requirement,safety-class/B" \
  --body "**Requirement ID**: REQ-006
**Source**: UN-001

The system shall manage clinical workflow lifecycle (create, transition, complete).

**Verification Method**: Unit Test + Integration Test
**Test Case(s)**: TC-006.1, TC-006.2, TC-006.3, TC-008.1
**Code Location**: \`src/azurioneye_operator/core/orchestrator.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-007] System shall validate all state transitions against allowed transition graph" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-007
**Source**: UN-001
**Safety-Critical**: Yes

The system shall validate all state transitions against the allowed transition graph. Invalid transitions shall be blocked and logged.

**Verification Method**: Unit Test
**Test Case(s)**: TC-007.1, TC-007.2, TC-007.3, TC-007.4, TC-RM-001.1
**Risk Item(s)**: RM-001
**Code Location**: \`src/azurioneye_operator/core/state_manager.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-008] System shall emit events on workflow state transitions" \
  --label "type/requirement,safety-class/B" \
  --body "**Requirement ID**: REQ-008
**Source**: UN-001

The system shall emit events on workflow state transitions for downstream consumers.

**Verification Method**: Unit Test
**Test Case(s)**: TC-008.1
**Code Location**: \`src/azurioneye_operator/core/orchestrator.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-009] System shall classify cardiac rhythm from ECG signal input" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-009
**Source**: UN-004
**Safety-Critical**: Yes

The system shall classify cardiac rhythm from ECG signal input data.

**Verification Method**: Unit Test
**Test Case(s)**: TC-009.1
**Risk Item(s)**: RM-003
**Code Location**: \`src/azurioneye_operator/api/predict.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-010] System shall return classification with confidence score" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-010
**Source**: UN-004, UN-005
**Safety-Critical**: Yes

The system shall return classification with confidence score. If confidence < 0.85, the response shall flag requires_human_review=true.

**Verification Method**: Unit Test
**Test Case(s)**: TC-010.1, TC-RM-003.1
**Risk Item(s)**: RM-003
**Code Location**: \`src/azurioneye_operator/api/predict.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-011] System shall reject inputs that fail validation" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-011
**Source**: UN-005
**Safety-Critical**: Yes

The system shall reject inputs that fail validation (signal length, lead name, signal quality).

**Verification Method**: Unit Test
**Test Case(s)**: TC-011.1, TC-011.2
**Risk Item(s)**: RM-005
**Code Location**: \`src/azurioneye_operator/api/predict.py\`"

gh issue create --repo "$REPO" \
  --title "[REQ-012] ML inference latency shall be less than 500ms" \
  --label "type/requirement,safety-class/B,safety-critical" \
  --body "**Requirement ID**: REQ-012
**Source**: UN-001
**Safety-Critical**: Yes

ML inference latency shall be <500ms per prediction.

**Verification Method**: Performance Test
**Test Case(s)**: TC-012.1
**Risk Item(s)**: RM-004
**Code Location**: \`src/azurioneye_operator/api/predict.py\`"

echo ""
echo "=== Step 5: Create Risk Item Issues ==="

gh issue create --repo "$REPO" \
  --title "[RM-001] Invalid clinical state transition" \
  --label "type/risk-item,risk-level/medium" \
  --body "**Risk ID**: RM-001
**Hazard**: Workflow engine allows clinically inappropriate state transition
**Harm**: Incorrect clinical application displayed, potential delayed treatment
**Severity**: Serious | **Probability**: Remote | **Pre-Mitigation**: MEDIUM

**Mitigation**: State machine validation (REQ-007) with explicit transition graph
**Linked Requirements**: #12 (REQ-007)
**Linked Test Cases**: TC-007.1, TC-007.2, TC-007.3, TC-007.4, TC-RM-001.1
**Post-Mitigation Risk**: LOW (acceptable)"

gh issue create --repo "$REPO" \
  --title "[RM-002] Lost workflow context" \
  --label "type/risk-item,risk-level/low" \
  --body "**Risk ID**: RM-002
**Hazard**: Workflow state or history lost during operation
**Harm**: Delayed clinical decisions, repeated manual steps
**Severity**: Minor | **Probability**: Occasional | **Pre-Mitigation**: LOW

**Mitigation**: Persistent state storage + audit log (REQ-002)
**Linked Requirements**: #7 (REQ-002)
**Linked Test Cases**: TC-006.1, TC-006.2, TC-008.1
**Post-Mitigation Risk**: LOW (acceptable)"

gh issue create --repo "$REPO" \
  --title "[RM-003] Incorrect cardiac rhythm classification" \
  --label "type/risk-item,risk-level/high" \
  --body "**Risk ID**: RM-003
**Hazard**: ML model returns wrong classification
**Hazardous Situation**: Clinician acts on incorrect rhythm assessment
**Harm**: Inappropriate treatment decision
**Severity**: Critical | **Probability**: Occasional | **Pre-Mitigation**: HIGH

**Mitigation**: Confidence threshold (0.85). Below threshold, requires_human_review=true. Classification is advisory only, never autonomous.
**Linked Requirements**: #15 (REQ-010)
**Linked Test Cases**: TC-009.1, TC-010.1, TC-RM-003.1
**Post-Mitigation Risk**: MEDIUM (ALARP, human-in-the-loop)"

gh issue create --repo "$REPO" \
  --title "[RM-004] Performance degradation" \
  --label "type/risk-item,risk-level/low" \
  --body "**Risk ID**: RM-004
**Hazard**: Inference or API latency exceeds 500ms threshold
**Harm**: Procedure time increased, patient under anesthesia longer
**Severity**: Minor | **Probability**: Occasional | **Pre-Mitigation**: LOW

**Mitigation**: Latency monitoring with alerting (REQ-005, REQ-012). Self-reported inference time in every response.
**Linked Requirements**: #10 (REQ-005), #17 (REQ-012)
**Linked Test Cases**: TC-012.1
**Post-Mitigation Risk**: LOW (acceptable)"

gh issue create --repo "$REPO" \
  --title "[RM-005] Data validation bypass" \
  --label "type/risk-item,risk-level/medium" \
  --body "**Risk ID**: RM-005
**Hazard**: Malformed clinical data processed without validation
**Harm**: Incorrect workflow state or classification
**Severity**: Serious | **Probability**: Remote | **Pre-Mitigation**: MEDIUM

**Mitigation**: Strict Pydantic validation on all API inputs (REQ-011). Signal quality assessment before inference.
**Linked Requirements**: #16 (REQ-011)
**Linked Test Cases**: TC-011.1, TC-011.2
**Post-Mitigation Risk**: LOW (acceptable)"

gh issue create --repo "$REPO" \
  --title "[RM-006] Service unavailability" \
  --label "type/risk-item,risk-level/low" \
  --body "**Risk ID**: RM-006
**Hazard**: AI Operator service crashes or becomes unresponsive
**Harm**: Manual fallback required, efficiency loss
**Severity**: Minor | **Probability**: Remote | **Pre-Mitigation**: LOW

**Mitigation**: Health check endpoints (REQ-003) for Kubernetes liveness/readiness probes. Graceful degradation.
**Linked Requirements**: #8 (REQ-003)
**Post-Mitigation Risk**: LOW (acceptable)"

echo ""
echo "=== Step 6: Create v0.1.0 release to trigger CI ==="
git tag -a v0.1.0 -m "v0.1.0 - Initial release for Ketryx evaluation"
git push origin v0.1.0

echo ""
echo "============================================"
echo "DONE! Repository is live at:"
echo "  https://github.com/${REPO}"
echo ""
echo "Next steps:"
echo "  1. Go to https://app.ketryx.com and connect the repo"
echo "  2. GitHub Actions will run automatically on the tag push"
echo "  3. Ketryx will start ingesting issues and CI artifacts"
echo "============================================"
