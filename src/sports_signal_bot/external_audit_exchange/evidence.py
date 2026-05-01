from typing import Dict, Any
from .contracts import ExternalVerificationDecisionRecord
import uuid

def create_evidence_from_decision(decision: ExternalVerificationDecisionRecord) -> Dict[str, Any]:
    return {
        "evidence_id": str(uuid.uuid4()),
        "source": "external_audit_exchange",
        "decision": decision.decision,
        "justification": decision.justification
    }
