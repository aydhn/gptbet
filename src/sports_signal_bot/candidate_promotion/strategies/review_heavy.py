from typing import List
from .base import BasePromotionStrategy
from ..contracts import CandidateReleaseRecord, CandidateManifest
from ..pipeline import run_candidate_pipeline

class ReviewHeavyPromotionStrategy(BasePromotionStrategy):
    """Makes extensive use of hold/revise for risky or mixed-evidence candidates."""
    def execute(self, candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
        return run_candidate_pipeline(candidates)
