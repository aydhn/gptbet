from typing import Dict, Any
from sports_signal_bot.sovereign_corridors.strategies.base import BaseSovereignCorridorStrategy

class TranslationStrictStrategy(BaseSovereignCorridorStrategy):
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "strategy": "TranslationStrictStrategy",
            "loss_tolerance": "none"
        }
