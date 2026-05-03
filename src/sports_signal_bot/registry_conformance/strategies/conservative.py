from typing import Dict, Any
from .base import RegistryConformanceStrategy


class ConservativeRegistryConformanceStrategy(RegistryConformanceStrategy):
    @property
    def name(self) -> str:
        return "ConservativeRegistryConformanceStrategy"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Strict currentness, validity, suppression. Low stale benchmark tolerance. Heavy conformance packs.
        context["strategy"] = self.name
        context["rules"] = {
            "strict_currentness": True,
            "stale_benchmark_tolerance": "low",
            "conformance_pack_weight": "heavy",
        }
        return context
