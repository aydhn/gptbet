
from typing import Dict, Any, List
from sports_signal_bot.reconciliation.strategies.base import ArbitrationStrategy
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class ReviewHeavyConflictStrategy(ArbitrationStrategy):
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:
        if not candidates:
            return None
        # Defers mostly to Conservative for now
        return list(candidates.values())[0]
