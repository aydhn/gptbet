from typing import List, Dict, Any, Optional
from sports_signal_bot.evidence.contracts import EvidenceClaimRecord, CitationTrailRecord

def build_claim(
    claim_id: str,
    claim_type: str,
    claim_text: str,
    support_strength: str,
    confidence_score: float,
    caveats: Optional[List[str]] = None
) -> EvidenceClaimRecord:
    status_map = {
        "high": "supported",
        "medium": "partially_supported",
        "low": "weakly_supported",
        "disputed": "contradicted",
        "unknown": "unresolved"
    }
    status = status_map.get(support_strength, "informational")

    return EvidenceClaimRecord(
        claim_id=claim_id,
        claim_type=claim_type,
        claim_text=claim_text,
        claim_status=status,
        support_strength=support_strength,
        confidence_score=confidence_score,
        caveats=caveats or []
    )

def attach_citations_to_claim(claim: EvidenceClaimRecord, citations: List[CitationTrailRecord]) -> EvidenceClaimRecord:
    for cit in citations:
        if cit.citation_id not in claim.citation_refs:
            claim.citation_refs.append(cit.citation_id)
    return claim
