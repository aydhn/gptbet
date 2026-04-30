from typing import List
from .base import BasePromotionStrategy
from ..contracts import CandidateReleaseRecord, CandidateManifest
from ..pipeline import run_candidate_pipeline

class FastLaneSafePatchStrategy(BasePromotionStrategy):
    """Optimized for very narrow, low-risk patches."""
    def execute(self, candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
        return run_candidate_pipeline(candidates)
