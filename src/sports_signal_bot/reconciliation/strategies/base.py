
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class ArbitrationStrategy(ABC):
    @abstractmethod
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:
        pass
