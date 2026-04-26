from typing import Dict, Any
from .registry import ThresholdStrategyRegistry
from .strategies.score_only import ScoreOnlyThresholdOptimizer
from .strategies.score_and_edge import ScoreAndEdgeThresholdOptimizer
from .strategies.conservative_quality import ConservativeQualityOptimizer
from .strategies.coverage_balanced import CoverageBalancedOptimizer
from .strategies.regime_placeholder import RegimeAwareThresholdPlaceholder
from .strategies.base import BaseThresholdOptimizer

ThresholdStrategyRegistry.register("score_only", ScoreOnlyThresholdOptimizer)
ThresholdStrategyRegistry.register("score_and_edge", ScoreAndEdgeThresholdOptimizer)
ThresholdStrategyRegistry.register("conservative_quality", ConservativeQualityOptimizer)
ThresholdStrategyRegistry.register("coverage_balanced", CoverageBalancedOptimizer)
ThresholdStrategyRegistry.register("regime_aware_placeholder", RegimeAwareThresholdPlaceholder)

class ThresholdStrategyFactory:
    @staticmethod
    def create(strategy_name: str, config: Dict[str, Any]) -> BaseThresholdOptimizer:
        strategy_class = ThresholdStrategyRegistry.get(strategy_name)
        return strategy_class(config)
