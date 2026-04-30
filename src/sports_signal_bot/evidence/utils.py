from typing import Dict, Any, List
import copy

def redact_evidence_payload(payload: Dict[str, Any], audience: str) -> Dict[str, Any]:
    if audience == "auditor_full":
        return payload.copy()

    redacted = copy.deepcopy(payload)

    def _redact_dict(d: dict):
        for k, v in d.items():
            if isinstance(k, str) and any(sec in k.lower() for sec in ["secret", "token", "password", "key"]):
                d[k] = "[REDACTED]"
            elif isinstance(v, dict):
                _redact_dict(v)
            elif isinstance(v, list):
                _redact_list(v)

    def _redact_list(l: list):
        for item in l:
            if isinstance(item, dict):
                _redact_dict(item)
            elif isinstance(item, list):
                _redact_list(item)

    _redact_dict(redacted)
    return redacted

def validate_claim_has_support(claim: Any) -> bool:
    if claim.claim_status in ["supported", "weakly_supported", "partially_supported"]:
        return True
    return False

def render_citation_summary(citations: List[Any]) -> str:
    summary = []
    for c in citations:
        summary.append(f"[{c.source_family}] {c.notes}")
    return " | ".join(summary)

def build_safe_citation_preview(citation: Any) -> str:
    return f"Ref: {citation.artifact_ref} from {citation.source_family}"

def enforce_audience_redaction_policy(bundle: Any, audience: str) -> Any:
    # A generic hook to enforce redaction over a full bundle
    return bundle

def scan_bundle_for_sensitive_leaks(bundle: Any) -> List[str]:
    # Hook for a security scan
    return []
