from typing import List, Tuple
from .base import BaseAssuranceStrategy
from ..contracts import ClaimFamily, PromotionEnvelopeRecord, AssuranceClaimRecord

class AttestationHeavyStrategy(BaseAssuranceStrategy):
    name: str = "attestation_heavy_strategy"

    def get_required_claim_families(self) -> List[ClaimFamily]:
        return [ClaimFamily.policy_conformance_claim]

    def evaluate_envelope(self, envelope: PromotionEnvelopeRecord, claims: List[AssuranceClaimRecord]) -> Tuple[bool, str]:
        if len(envelope.assurance_attestations) < len(envelope.satisfied_claims):
            return False, "Not enough attestations for satisfied claims."
        return True, "Passed."
