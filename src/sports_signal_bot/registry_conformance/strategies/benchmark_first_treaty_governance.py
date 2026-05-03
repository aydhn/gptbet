from typing import Dict, Any
from .base import RegistryConformanceStrategy


class BenchmarkFirstTreatyGovernanceStrategy(RegistryConformanceStrategy):
    @property
    def name(self) -> str:
        return "BenchmarkFirstTreatyGovernanceStrategy"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["strategy"] = self.name
        context["rules"] = {
            "strict_currentness": True,
            "stale_benchmark_tolerance": "none",
            "conformance_pack_weight": "balanced",
            "treaty_lifecycle_weight": "heavy",
        }
        return context
