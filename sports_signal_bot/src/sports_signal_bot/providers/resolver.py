from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.requests import ProviderRequestRecord
from sports_signal_bot.providers.routing import (
    CachedFirstForPreviewStrategy,
    ConservativeOpsProviderStrategy,
    PrimaryThenFallbackStrategy,
    QualityWeightedRoutingStrategy,
    StableProviderPreferredStrategy,
)


class ProviderResolver:
    def __init__(
        self, registry_data: List[Dict[str, Any]], config: Dict[str, Any] = None
    ):
        self.registry_data = registry_data
        self.config = config or {}

    def resolve(self, request: ProviderRequestRecord) -> List[str]:
        mode = request.mode
        strategy_name = self.config.get("routing_strategy_by_mode", {}).get(
            mode, "primary_then_fallback"
        )

        if strategy_name == "quality_weighted":
            strategy = QualityWeightedRoutingStrategy()
        elif strategy_name == "stable_preferred":
            strategy = StableProviderPreferredStrategy()
        elif strategy_name == "cached_first":
            strategy = CachedFirstForPreviewStrategy()
        elif strategy_name == "conservative_ops":
            strategy = ConservativeOpsProviderStrategy()
        else:
            strategy = PrimaryThenFallbackStrategy()

        return strategy.select_providers(request, self.registry_data)
