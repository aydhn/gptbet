from abc import ABC, abstractmethod
from typing import Dict, Any
from ..contracts import CandidateInputRecord, AutoProgressionDecisionRecord

class BasePromotionStrategy(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate_candidate(self, candidate: CandidateInputRecord, engine) -> AutoProgressionDecisionRecord:
        pass
