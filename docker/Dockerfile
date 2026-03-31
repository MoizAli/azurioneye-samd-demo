# Multi-stage build for AzurionEye AI Operator
# IEC 62304: Reproducible builds with pinned dependencies

FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim as production

LABEL maintainer="Philips IGT-S"
LABEL description="AzurionEye AI Operator - SaMD IEC 62304 Class B"
LABEL version="0.1.0"

# Security: non-root user
RUN useradd --create-home --shell /bin/bash azurioneye
WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ ./src/

USER azurioneye

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')"

CMD ["uvicorn", "src.azurioneye_operator.main:app", "--host", "0.0.0.0", "--port", "8000"]
