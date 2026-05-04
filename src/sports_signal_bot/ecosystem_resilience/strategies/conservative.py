from sports_signal_bot.ecosystem_resilience.strategies.base import BaseEcosystemResilienceStrategy

class ConservativeTrustOverlayStrategy(BaseEcosystemResilienceStrategy):
    name = "conservative"

    def evaluate(self, context: dict) -> dict:
        return {"decision": "review_only"}
