from typing import Dict, Any, List
from .contracts import ExternalAuditResponseRecord, ExternalVerificationImportRecord
import uuid
import datetime

def ingest_external_response(response: ExternalAuditResponseRecord) -> ExternalVerificationImportRecord:
    status = "imported_pending_verification"
    return ExternalVerificationImportRecord(
        import_id=str(uuid.uuid4()),
        external_response_id=response.external_response_id,
        status=status
    )

def validate_external_response_schema(raw_response: Dict[str, Any]) -> bool:
    required_keys = ["external_response_id", "request_id", "responder_family", "response_status", "trust_level_claimed"]
    for key in required_keys:
        if key not in raw_response:
            return False
    return True

def evaluate_external_response_trust(response: ExternalAuditResponseRecord, responder_reputation: float) -> str:
    if responder_reputation < 30:
        return "untrusted"
    if response.trust_level_claimed == "high" and responder_reputation >= 80:
        return "trusted"
    return "conditional"

def normalize_external_findings(raw_findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for f in raw_findings:
        nf = f.copy()
        if "severity" not in nf:
            nf["severity"] = "info"
        normalized.append(nf)
    return normalized

def decide_external_response_outcome(import_record: ExternalVerificationImportRecord, trust_eval: str) -> str:
    if trust_eval == "untrusted":
        import_record.status = "imported_quarantined"
        import_record.local_actions.append("quarantine")
        return "quarantined"
    elif trust_eval == "trusted":
        import_record.status = "imported_verified_supporting"
        import_record.local_actions.append("add_supporting_evidence")
        return "verified_supporting"

    import_record.status = "imported_pending_verification"
    import_record.local_actions.append("open_review_case")
    return "review"
