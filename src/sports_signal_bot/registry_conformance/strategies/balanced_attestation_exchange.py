from typing import Dict, Any
from .base import RegistryConformanceStrategy


class BalancedAttestationExchangeStrategy(RegistryConformanceStrategy):
    @property
    def name(self) -> str:
        return "BalancedAttestationExchangeStrategy"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["strategy"] = self.name
        context["rules"] = {
            "strict_currentness": False,
            "stale_benchmark_tolerance": "medium",
            "conformance_pack_weight": "balanced",
        }
        return context
