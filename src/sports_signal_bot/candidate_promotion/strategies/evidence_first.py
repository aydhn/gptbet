from typing import List
from .base import BasePromotionStrategy
from ..contracts import CandidateReleaseRecord, CandidateManifest
from ..pipeline import run_candidate_pipeline

class EvidenceFirstCandidatePromotionStrategy(BasePromotionStrategy):
    """Prioritizes evidence completeness and support over simulation benefit."""
    def execute(self, candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
        return run_candidate_pipeline(candidates)
