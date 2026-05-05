from typing import Dict, Any
from .base import BasePerformanceHardeningStrategy

class CacheSafetyFirstStrategy(BasePerformanceHardeningStrategy):
    def evaluate_envelope(self, target_ref: str) -> Dict[str, Any]:
        return {"status": "within_budget", "max_latency": 150}

    def get_cache_ttl(self, family: str) -> int:
        return 30
