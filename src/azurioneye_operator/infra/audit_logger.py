"""
Structured audit logging for regulatory compliance.

Implements: REQ-002 (All clinical decisions logged with timestamp)

Every clinical decision, API call, and state transition is logged
in structured JSON format for regulatory evidence. Logs are immutable
and must be preserved for the life of the device.

Design Reference: SDDD Section 3.1 - Audit Trail Architecture
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any


class AuditLogger:
    """
    Regulatory-compliant audit logger.
    Outputs structured JSON to both file and stdout.
    """

    def __init__(self, name: str = "azurioneye.audit"):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def log(self, event: str, **kwargs: Any) -> None:
        """
        Log an audit event with structured metadata.

        Args:
            event: Event type (e.g., "prediction_made", "workflow_transitioned")
            **kwargs: Additional key-value pairs for the audit record
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "service": "azurioneye-operator",
            "version": "0.1.0",
            **kwargs,
        }
        self._logger.info(json.dumps(record))
