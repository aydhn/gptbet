from typing import List, Tuple
from .base import BaseAssuranceStrategy
from ..contracts import ClaimFamily, PromotionEnvelopeRecord, AssuranceClaimRecord

class ReplayFirstAssuranceStrategy(BaseAssuranceStrategy):
    name: str = "replay_first_strategy"

    def get_required_claim_families(self) -> List[ClaimFamily]:
        return [ClaimFamily.policy_conformance_claim]

    def evaluate_envelope(self, envelope: PromotionEnvelopeRecord, claims: List[AssuranceClaimRecord]) -> Tuple[bool, str]:
        if "deterministic_seed" not in envelope.replay_hints:
            return False, "Replay hints must contain deterministic_seed."
        return True, "Passed."
