from typing import Dict, Any
from .base import BasePerformanceHardeningStrategy

class HotPathFirstStrategy(BasePerformanceHardeningStrategy):
    def evaluate_envelope(self, target_ref: str) -> Dict[str, Any]:
        return {"status": "within_budget", "max_latency": 50}

    def get_cache_ttl(self, family: str) -> int:
        return 120
