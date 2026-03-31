# AzurionEye AI Operator - SaMD Demo Repository

**Purpose**: Dummy medical device software repository for evaluating [Ketryx](https://ketryx.com) as compliance orchestration layer.

**Safety Classification**: IEC 62304 Class B
**Regulatory Pathway**: FDA 510(k) + PCCP (Predetermined Change Control Plan)
**Product**: AzurionEye AI Operator + Orchestrator (Software as Medical Device)

---

## What This Repository Demonstrates

This is a realistic (but fictional) SaMD repository designed to show end-to-end Ketryx integration across the full IEC 62304 lifecycle:

1. **Requirements Management** - GitHub Issues as design inputs, auto-linked to Ketryx traceability
2. **Design Controls** - PR templates with IEC 62304 review checklists
3. **Verification & Validation** - Pytest suites mapped to software requirements
4. **Risk Management** - ISO 14971 risk items tracked as issues, linked to mitigating tests
5. **Release Management** - 7-gate automated compliance checklist via Ketryx
6. **SBOM/SOUP** - Auto-generated from dependency files using CycloneDX
7. **Traceability** - Live matrix: User Needs -> Design Inputs -> Requirements -> Code -> Tests

## Quick Start

```bash
# Clone and set up
git clone https://github.com/philips-internal/azurioneye-samd-demo.git
cd azurioneye-samd-demo
pip install -r requirements.txt

# Run tests (generates verification evidence)
pytest --cov=src --cov-report=html --junitxml=test-results.xml

# Run the service
uvicorn src.azurioneye_operator.main:app --reload

# Generate SBOM
bash scripts/generate-sbom.sh
```

## Repository Structure

```
azurioneye-samd-demo/
├── .github/              # CI/CD workflows + issue/PR templates (Ketryx integration points)
├── .ketryx/              # Ketryx configuration, sync mapping, release gates
├── src/                  # Production code (FastAPI service + ML inference)
├── tests/                # Unit, integration, compliance test suites
├── docs/                 # IEC 62304 QMS artifacts + architecture docs
├── config/               # Build, test, security configurations
├── scripts/              # SBOM generation, compliance reporting
└── docker/               # Container configuration
```

## Compliance Framework

| Standard | Coverage | Evidence Location |
|----------|----------|-------------------|
| IEC 62304 | Class B lifecycle | `docs/qms/`, GitHub Issues, CI/CD |
| ISO 14971 | Risk management | `docs/qms/Risk_Management_File.md`, GitHub Issues (label: `risk-item`) |
| FDA PCCP | AI/ML change control | `docs/compliance/pccp-change-protocol.md` |
| IEC 82304-1 | Health software | `docs/qms/Software_Development_Plan.md` |

## Ketryx Integration

See `.ketryx/config.yaml` for the full integration configuration. Key sync points:

- **Issues -> Requirements**: Bidirectional sync via webhook
- **PRs -> Design Reviews**: Auto-ingested as review evidence
- **CI Test Results -> Verification**: JUnit XML ingested per build
- **Releases -> DHF Assembly**: Tag triggers document generation

## Team

| Role | Person | Responsibility |
|------|--------|---------------|
| QMS Lead | Amit | QMS artifact templates, compliance review |
| Regulatory | Marlies | 510(k) submission, intended use |
| Platform Engineering | Patrick Bronneberg | CI/CD, infrastructure |
| Architecture | Eric Suijs | Technical decomposition |
| ALM/CodeBeamer | David Munich | Information model mapping |
