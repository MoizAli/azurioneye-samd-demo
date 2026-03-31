.PHONY: install test lint coverage sbom run clean

# Developer convenience targets
install:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=xml:coverage.xml --junitxml=test-results.xml -v
	@echo "Coverage report: htmlcov/index.html"

sbom:
	cyclonedx-py requirements -i requirements.txt -o sbom.json --format json
	pip-licenses --format=json --output-file=licenses.json
	@echo "SBOM: sbom.json | Licenses: licenses.json"

security:
	safety check -r requirements.txt
	bandit -r src/ -ll

run:
	uvicorn src.azurioneye_operator.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf htmlcov/ .coverage coverage.xml test-results*.xml sbom.json licenses.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
