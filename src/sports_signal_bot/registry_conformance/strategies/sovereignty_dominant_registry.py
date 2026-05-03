from typing import Dict, Any
from .base import RegistryConformanceStrategy


class SovereigntyDominantRegistryStrategy(RegistryConformanceStrategy):
    @property
    def name(self) -> str:
        return "SovereigntyDominantRegistryStrategy"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["strategy"] = self.name
        context["rules"] = {
            "sovereignty_suppression": "dominant",
            "exchange_visibility": "narrow",
        }
        return context
