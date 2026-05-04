from sports_signal_bot.ecosystem_resilience.strategies.base import BaseEcosystemResilienceStrategy

class MarketplaceSignalStrictStrategy(BaseEcosystemResilienceStrategy):
    name = "marketplace_signal_strict"

    def evaluate(self, context: dict) -> dict:
        return {"decision": "suppress_stale"}
