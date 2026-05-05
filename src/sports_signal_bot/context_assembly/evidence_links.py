from .contracts import ContextEvidenceLinkRecord
import uuid

def create_evidence_link(evidence_ref: str) -> ContextEvidenceLinkRecord:
    return ContextEvidenceLinkRecord(
        link_id=f"el_{uuid.uuid4().hex[:8]}",
        evidence_ref=evidence_ref
    )
