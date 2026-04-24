from typing import Dict, Any, List
from .base import BaseEnsembler
from .weighted_average import WeightedAverageEnsembler
from .best_source_fallback import BestSourceFallbackEnsembler
from ..contracts import EnsembleInputRecord, EnsembleOutputRecord

class RuleBasedHybridEnsembler(BaseEnsembler):

    def __init__(self, name: str = "rule_based_hybrid", config: Dict[str, Any] = None):
        super().__init__(name, config)
        self.rules = self.config.get("rules", {})
        self.default_strategy = self.config.get("default_strategy", "simple_average")

    def combine(self, input_record: EnsembleInputRecord) -> EnsembleOutputRecord:

        # Determine strategy based on sport/market
        key = f"{input_record.sport}_{input_record.market_type}"
        strategy_name = self.rules.get(key, self.default_strategy)

        # Instantiate sub-ensembler (In a real system, you'd use a registry/factory here)
        # For simplicity in this phase, we hardcode the mapping
        from .simple_average import SimpleAverageEnsembler

        if strategy_name == "weighted_average":
            sub_ensembler = WeightedAverageEnsembler("weighted_average", self.config)
        elif strategy_name == "best_source_fallback":
            sub_ensembler = BestSourceFallbackEnsembler("best_source_fallback", self.config)
        else:
            sub_ensembler = SimpleAverageEnsembler("simple_average", self.config)

        output = sub_ensembler.combine(input_record)
        output.ensemble_name = f"{self.name}({strategy_name})"
        return output
