from datetime import datetime
from typing import Dict, Any
from .contracts import CohortEvidenceRecord

def build_growth_evidence_packet(cohort_id: str, payload: Dict[str, Any]) -> CohortEvidenceRecord:
    return CohortEvidenceRecord(
        evidence_id=f"ev_gr_{cohort_id}",
        cohort_id=cohort_id,
        evidence_type="growth_evidence",
        payload=payload
    )

def explain_cohort_progression(cohort_id: str, rationale: str) -> dict:
    return {
        "cohort_id": cohort_id,
        "action": "progression",
        "rationale": rationale
    }

def explain_pause_shrink_rollback(cohort_id: str, action: str, rationale: str) -> dict:
    return {
        "cohort_id": cohort_id,
        "action": action,
        "rationale": rationale
    }

def attach_verification_citations(cohort_id: str, citations: list) -> dict:
    return {
        "cohort_id": cohort_id,
        "citations": citations
    }
