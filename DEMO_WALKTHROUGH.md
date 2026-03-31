# Ketryx End-to-End Demo Walkthrough
## AzurionEye SaMD Repository + Ketryx Compliance Orchestration

**Duration**: 25-30 minutes
**Audience**: Amit (QMS), Marlies (Regulatory), Patrick (Engineering), David Munich (CodeBeamer/ALM), Marion (R&D Lead)
**Goal**: Demonstrate that GitHub + Ketryx can replace the 3-layer model (Notion + GitHub + CodeBeamer) with a 2-layer model that's faster, more automated, and equally compliant.

---

## Pre-Demo Setup

1. Repository pushed to GitHub (philips-internal/azurioneye-samd-demo)
2. Ketryx sandbox connected to the repository
3. GitHub Issues pre-populated with REQ-001 through REQ-008 and RM-001 through RM-004
4. CI/CD pipelines have run at least once (green builds)
5. One release (v0.1.0) already completed as baseline

---

## Act 1: The Problem (3 minutes)

**Talking point**: "Today we maintain traceability across three disconnected systems. A single requirement change touches Notion, GitHub, and CodeBeamer. This demo shows what it looks like when compliance flows naturally from engineering work."

Show the current 3-layer diagram:
```
Notion (product)  -->  GitHub (code)  -->  CodeBeamer (compliance)
     Manual sync           Manual sync          Manual sync
```

Then show the proposed 2-layer:
```
GitHub (engineering source of truth)
         |
    Ketryx (compliance orchestration, auto-sync)
```

---

## Act 2: New Feature, Start to Finish (15 minutes)

### Scene 1: User Need Arrives (2 min)

1. **Create GitHub Issue**: User Need UN-005
   - Title: "[UN-005] Cardiologists need real-time procedure metrics dashboard"
   - Label: `type/user-need`

2. **Show Ketryx**: Within seconds, Ketryx ingests the issue and creates a User Need record in the compliance view.

3. **Ketryx AI**: Suggest design inputs from the user need. Ketryx proposes:
   - "DI-005: Dashboard shall display hemodynamic parameters in real-time"
   - Human reviews and accepts.

### Scene 2: Requirements Created (3 min)

1. **Create 3 GitHub Issues** from the design input:
   - REQ-010: "System shall display procedure metrics via WebSocket endpoint"
   - REQ-011: "Metrics update interval shall be <= 500ms"
   - REQ-012: "Dashboard access shall require operator authentication"
   - All labeled `type/requirement`, linked to UN-005

2. **Show Ketryx traceability**: UN-005 -> DI-005 -> REQ-010, REQ-011, REQ-012
   - Ketryx flags: "3 requirements with 0 test cases" (warning icon)
   - This is the gap analysis that currently requires manual CodeBeamer checking

### Scene 3: Ketryx AI Suggests Test Cases (2 min)

1. **Ketryx AI Assistant**: For REQ-010, suggests:
   - TC-010.1: "Unit test: WebSocket endpoint returns metrics JSON"
   - TC-010.2: "Integration test: metrics update under load"
   - TC-010.3: "Performance test: update interval <= 500ms"

2. **Human approves**: Developer accepts suggestions. Ketryx auto-creates test case issues in GitHub with proper labels and links.

3. **Show traceability update**: REQ-010 now shows "3 test cases linked" (green check)

### Scene 4: Developer Implements (3 min)

1. **Show the PR**: Developer creates branch, writes code with REQ-010 references in docstrings, writes tests with TC-010 references.

2. **PR Template**: Show the IEC 62304 design review checklist in the PR. All items checked.

3. **CI runs**: Tests pass, coverage at 84%.

4. **Show Ketryx**:
   - PR automatically ingested as design review evidence
   - Test results (JUnit XML) auto-ingested as verification evidence
   - Traceability matrix updated: REQ-010 -> code (PR #XX) -> TC-010.1 PASS

### Scene 5: Risk Integration (2 min)

1. **Create risk item**: RM-004 "Performance degradation under concurrent load"
   - Severity: Minor, Probability: Occasional, Risk: LOW
   - Link to REQ-011 and TC-010.2

2. **Show Ketryx**:
   - Risk item synced from GitHub
   - Linked to requirement and test case
   - Since TC-010.2 PASSED in CI, Ketryx auto-marks: "RM-004: VERIFIED"
   - This is real-time; no manual documentation needed

### Scene 6: Merge (1 min)

1. **Merge PR**: All checks green, design review complete.
2. **Show Ketryx audit trail**: Complete evidence chain from user need to verified code.

---

## Act 3: Release with Compliance Gates (7 minutes)

### Scene 7: Cut a Release (3 min)

1. **Tag release**: `git tag v0.2.0 && git push --tags`

2. **GitHub Actions fires**: Release workflow runs all 5 gates:
   - All tests pass
   - Coverage >= 80%
   - Security scan clean
   - SBOM generated
   - Release notes generated

3. **Show Ketryx release dashboard**: 7-gate compliance checklist:

   | Gate | Status | Evidence |
   |------|--------|----------|
   | Design Review | PASS | All PRs approved |
   | Requirements Coverage | PASS | 12/12 requirements verified |
   | Risk Assessment | PASS | All HIGH risks verified |
   | Code Coverage | PASS | 84% (>= 80%) |
   | Security Scan | PASS | No CRITICAL CVEs |
   | SOUP Declaration | PASS | SBOM reviewed |
   | Release Notes | PASS | Completed |

### Scene 8: Auto-Generated Documents (2 min)

1. **Ketryx auto-generates** on release:
   - Code Review Report (aggregated from all PR reviews)
   - Traceability Matrix (complete, live)
   - Risk Management Summary (all risks with verification status)
   - SBOM/SOUP Report (from CycloneDX)
   - Release Notes

2. **Show a generated document**: Open the traceability matrix. It shows the complete chain from UN-001 through REQ-001 through TC-001.1 with PASS evidence from build #XX.

3. **Key message**: "These documents would take days to compile manually in CodeBeamer. Ketryx generates them in seconds from the same data that already exists in GitHub."

### Scene 9: The Big Picture (2 min)

1. **Show Ketryx dashboard**: Full product overview
   - All user needs traced to verified requirements
   - All risks mitigated and verified
   - Release history with compliance bundles
   - Real-time traceability (no stale data)

2. **The question for the room**: "Does this give you what CodeBeamer gives you, faster?"

---

## Act 4: Questions We Need to Answer (5 minutes)

Facilitate discussion on these open items:

1. **Notion gap**: Ketryx doesn't integrate with Notion natively. Do we need a bridge, or do we move product definition work to GitHub Projects/Jira?

2. **CodeBeamer coexistence**: Can Ketryx and CodeBeamer run in parallel during transition? Or is it one or the other?

3. **Philips existing Ketryx relationship**: Kevin confirmed Philips is already a Ketryx partner. Who owns this relationship internally? Can we leverage it?

4. **David Munich's information model**: How does Ketryx's data model map to the CodeBeamer information model David has defined?

5. **Windchill integration**: Existing QMS baseline is in PTC Windchill. Does Ketryx need to interface with Windchill, or is it a clean replacement for the software layer?

6. **NDA and deeper evaluation**: Next step is NDA with Ketryx for access to full feature set and Philips-specific configuration.

---

## Post-Demo Next Steps

- [ ] Schedule 30-min deep dive with Kevin Schurr (Ketryx) + AzurionEye engineering team
- [ ] Find Philips internal Ketryx relationship owner
- [ ] Map Amit's QMS artifact templates to Ketryx document templates
- [ ] Evaluate Ketryx sandbox with real (anonymized) AzurionEye requirements
- [ ] Compare Ketryx total cost vs. CodeBeamer license + integration effort
- [ ] Decision: proceed with Ketryx PoC or stay with CodeBeamer (target: Sprint 6)
