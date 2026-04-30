from abc import ABC, abstractmethod
from typing import List
from ..contracts import CandidateReleaseRecord, CandidateManifest

class BasePromotionStrategy(ABC):
    @abstractmethod
    def execute(self, candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
        pass
