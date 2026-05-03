from typing import Dict, Any
from .base import RegistryConformanceStrategy


class PackStrictStrategy(RegistryConformanceStrategy):
    @property
    def name(self) -> str:
        return "PackStrictStrategy"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["strategy"] = self.name
        context["rules"] = {
            "conformance_pack_gaps": "very_strict",
            "discoverability_drop_rate": "fast",
        }
        return context
