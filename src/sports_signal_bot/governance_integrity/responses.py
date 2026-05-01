from typing import Dict, Any, List
import uuid
from datetime import datetime

from .contracts import IntegrityFailureRecord

class IntegrityTamperResponder:
    """Handles responses to integrity failures."""
    def __init__(self):
        self.failures: List[IntegrityFailureRecord] = []

    def respond_to_integrity_failure(
        self,
        reason: str,
        affected_refs: List[str],
        context: Dict[str, Any],
        severity: str = "critical"
    ) -> IntegrityFailureRecord:
        """Records an integrity failure and triggers responses."""
        record = IntegrityFailureRecord(
            failure_id=f"fail_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            severity=severity,
            reason=reason,
            affected_refs=affected_refs,
            context=context
        )
        self.failures.append(record)

        # Here we would emit an alert to monitoring
        print(f"[ALERT] {severity.upper()} Integrity Failure: {reason} - Refs: {affected_refs}")

        return record

_global_responder = IntegrityTamperResponder()

def get_tamper_responder() -> IntegrityTamperResponder:
    return _global_responder
