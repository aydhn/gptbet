from typing import Any, Dict

from sports_signal_bot.signal_scoring.registry import SignalScorerRegistry
from sports_signal_bot.signal_scoring.strategies import (
    BalancedSignalScorer, BaseSignalScorer, ConservativeQualityScorer,
    EdgeFocusedScorer, NoMarketReferenceFallbackScorer,
    RegimeAwareSignalScorer)

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
