from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import CouncilDecisionType, CouncilVoteLikeRecord

class BaseHandoffStrategy(ABC):
    @abstractmethod
    def evaluate(self, context: Dict[str, Any], votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
        pass
