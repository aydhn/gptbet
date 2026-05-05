"""
Base hardening strategy.
"""
from typing import Dict, Any

class BaseHardeningStrategy:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
