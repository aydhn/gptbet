from typing import List
from .base import BasePromotionStrategy
from ..contracts import CandidateReleaseRecord, CandidateManifest
from ..pipeline import run_candidate_pipeline

class ConservativeCandidatePromotionStrategy(BasePromotionStrategy):
    """Conservative strategy with strict safety filters and heavy approval requirements."""
    def execute(self, candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
        return run_candidate_pipeline(candidates)
