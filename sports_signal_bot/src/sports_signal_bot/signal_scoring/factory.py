from typing import Dict, Any

from sports_signal_bot.signal_scoring.strategies import (
    EdgeFocusedScorer, BalancedSignalScorer, ConservativeQualityScorer,
    RegimeAwareSignalScorer, NoMarketReferenceFallbackScorer, BaseSignalScorer
)
from sports_signal_bot.signal_scoring.registry import SignalScorerRegistry

# Register available strategies
SignalScorerRegistry.register("edge_focused", EdgeFocusedScorer)
SignalScorerRegistry.register("balanced", BalancedSignalScorer)
SignalScorerRegistry.register("conservative_quality", ConservativeQualityScorer)
SignalScorerRegistry.register("regime_aware", RegimeAwareSignalScorer)
SignalScorerRegistry.register("no_market_reference", NoMarketReferenceFallbackScorer)

class SignalScorerFactory:

    @staticmethod
    def create(strategy_name: str, config: Dict[str, Any]) -> BaseSignalScorer:
        strategy_class = SignalScorerRegistry.get(strategy_name)
        return strategy_class(config)
