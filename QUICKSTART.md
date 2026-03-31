# AzurionEye SaMD Demo - Quick Start

## What you have

A complete IEC 62304 Class B repository with:
- FastAPI service (clinical workflow orchestration + ML inference)
- 37 passing tests (unit, integration, compliance)
- 7 QMS documents (SDP, SRS, SADD, V&V, RMF, SOUP, Traceability)
- 4 GitHub Actions workflows (CI, security, SBOM, release)
- Ketryx config with 7-gate release checklist
- GitHub issue/PR templates for regulatory traceability

## Setup (5 minutes)

### Prerequisites
```bash
brew install gh git
gh auth login   # authenticate with your GitHub account
```

### Step 1: Push to GitHub

The repo `MoizAli/azurioneye-samd-demo` already exists on GitHub. From this directory:

```bash
git remote add origin https://github.com/MoizAli/azurioneye-samd-demo.git
git push -u origin main --force
```

### Step 2: Create labels + issues + release tag

```bash
./setup_github.sh
```

This creates:
- 16 labels (requirement types, safety classes, risk levels, verification status)
- 5 User Need issues (UN-001 through UN-005)
- 12 Requirement issues (REQ-001 through REQ-012) with safety classifications
- 6 Risk Item issues (RM-001 through RM-006) with FMEA structure
- v0.1.0 release tag (triggers CI automatically)

### Step 3: Verify CI

Go to https://github.com/MoizAli/azurioneye-samd-demo/actions and confirm:
- CI Tests workflow runs and passes
- Security Scan runs
- SBOM Generation runs on the release
- Release workflow creates v0.1.0 with compliance bundle

### Step 4: Connect Ketryx

1. Go to https://app.ketryx.com (use Kevin Schurr's sandbox invite)
2. Connect the `MoizAli/azurioneye-samd-demo` repository
3. Ketryx will auto-ingest all GitHub Issues as requirements/risks
4. CI artifacts (JUnit XML, coverage, SBOM) become compliance evidence

## Running Tests Locally

```bash
make install   # install deps
make test      # run all 37 tests
make coverage  # run with coverage report
make lint      # run linters
make security  # run security scans
```

## Demo Walkthrough

See `DEMO_WALKTHROUGH.md` for the full 25-minute demo script covering:
- Act 1: The Problem (3-layer vs 2-layer)
- Act 2: New Feature, Start to Finish (user need through verified code)
- Act 3: Release with Compliance Gates (7-gate checklist)
- Act 4: Questions for the Room
