from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..contracts import AutopilotDecisionRecord, ActivationLevel, AdoptionCohortRecord

class BaseCohortAutopilotStrategy(ABC):
    @abstractmethod
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        pass
