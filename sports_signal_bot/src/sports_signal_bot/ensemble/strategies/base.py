from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..contracts import EnsembleInputRecord, EnsembleOutputRecord, StandardizedPredictionRecord

class BaseEnsembler(ABC):

    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}

    @abstractmethod
    def combine(self, input_record: EnsembleInputRecord) -> EnsembleOutputRecord:
        """Combines multiple predictions for a single event/market into a final output."""
        pass

    def combine_batch(self, input_records: List[EnsembleInputRecord]) -> List[EnsembleOutputRecord]:
        """Combines predictions for a batch of events."""
        return [self.combine(rec) for rec in input_records]

    def fit(self, metadata: Optional[Dict[str, Any]] = None):
        """Optional fitting method for stateful ensemblers."""
        pass

    def describe(self) -> Dict[str, Any]:
        """Returns description of the ensembler strategy."""
        return {
            "name": self.name,
            "config": self.config
        }
