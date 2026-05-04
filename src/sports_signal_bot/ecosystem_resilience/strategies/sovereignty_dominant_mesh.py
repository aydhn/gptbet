from sports_signal_bot.ecosystem_resilience.strategies.base import BaseEcosystemResilienceStrategy

class SovereigntyDominantMeshStrategy(BaseEcosystemResilienceStrategy):
    name = "sovereignty_dominant"

    def evaluate(self, context: dict) -> dict:
        return {"decision": "sovereignty_override"}
