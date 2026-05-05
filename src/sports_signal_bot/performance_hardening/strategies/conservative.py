from typing import Dict, Any
from .base import BasePerformanceHardeningStrategy

class ConservativePerformanceHardeningStrategy(BasePerformanceHardeningStrategy):
    def evaluate_envelope(self, target_ref: str) -> Dict[str, Any]:
        return {"status": "within_budget_with_caveats", "max_latency": 100}

    def get_cache_ttl(self, family: str) -> int:
        return 60
