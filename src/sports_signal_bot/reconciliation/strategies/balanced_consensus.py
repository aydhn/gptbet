
from typing import Dict, Any, List
from collections import Counter
from sports_signal_bot.reconciliation.strategies.base import ArbitrationStrategy
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

class BalancedConsensusStrategy(ArbitrationStrategy):
    def resolve_field(self, field_name: str, candidates: Dict[str, Any], observations: List[SourceObservationRecord]) -> Any:
        if not candidates:
            return None

        values = list(candidates.values())
        counts = Counter(values)

        # Simple majority wins
        most_common = counts.most_common(1)
        if most_common:
            return most_common[0][0]

        return values[0]
