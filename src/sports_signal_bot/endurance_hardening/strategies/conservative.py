from typing import Dict, Any
from .base import EnduranceHardeningStrategy

class ConservativeEnduranceHardeningStrategy(EnduranceHardeningStrategy):
    @property
    def strategy_name(self) -> str:
        return "ConservativeEnduranceHardeningStrategy"

    def evaluate_endurance(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "blocked", "reason": "Slightest drift detected (simulated)"}
