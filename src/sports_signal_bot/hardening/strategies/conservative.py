"""
ConservativeHardeningStrategy.
"""
from .base import BaseHardeningStrategy
from typing import Dict, Any

class ConservativeHardeningStrategy(BaseHardeningStrategy):
    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "ConservativeHardeningStrategy", "strictness": "high", "block_on_any_mismatch": True}
