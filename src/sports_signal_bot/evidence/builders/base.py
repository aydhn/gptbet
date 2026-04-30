from typing import Dict, Any, List
from sports_signal_bot.evidence.contracts import EvidenceBundleRecord, EvidenceClaimRecord, CitationTrailRecord

class BaseEvidenceBuilder:
    def __init__(self, target_entity_type: str, target_entity_id: str, audience_profile: str):
        self.target_entity_type = target_entity_type
        self.target_entity_id = target_entity_id
        self.audience_profile = audience_profile
        self.claims: List[EvidenceClaimRecord] = []
        self.citations: List[CitationTrailRecord] = []

    def add_claim(self, claim: EvidenceClaimRecord):
        self.claims.append(claim)

    def add_citation(self, citation: CitationTrailRecord):
        self.citations.append(citation)

    def build(self) -> EvidenceBundleRecord:
        from sports_signal_bot.evidence.confidence import compute_bundle_confidence

        bundle = EvidenceBundleRecord(
            bundle_id=f"bundle_{self.target_entity_id}",
            bundle_type=self.__class__.__name__,
            target_entity_type=self.target_entity_type,
            target_entity_id=self.target_entity_id,
            audience_profile=self.audience_profile,
            evidence_status="draft",
            confidence_band="unknown",
            claims=self.claims,
            citations=self.citations
        )
        bundle.confidence_band = compute_bundle_confidence(bundle)
        bundle.evidence_status = "ready"
        return bundle
