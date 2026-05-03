from typing import Dict, Any
from sports_signal_bot.sovereign_corridors.strategies.base import BaseSovereignCorridorStrategy

class ContinuityFirstStrategy(BaseSovereignCorridorStrategy):
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "strategy": "ContinuityFirstStrategy",
            "visibility_bias": "low",
            "gap_tolerance": "none"
        }
