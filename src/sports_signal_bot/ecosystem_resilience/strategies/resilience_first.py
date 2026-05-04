from sports_signal_bot.ecosystem_resilience.strategies.base import BaseEcosystemResilienceStrategy

class ResilienceFirstEcosystemStrategy(BaseEcosystemResilienceStrategy):
    name = "resilience_first"

    def evaluate(self, context: dict) -> dict:
        return {"decision": "degrade_if_pressure"}
