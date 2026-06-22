from typing import Any, Dict

from .base import BaseGeoStrategy


class BalancedGeoReadinessStrategy(BaseGeoStrategy):
    def check_lag(self, lag: int) -> str:
        if lag > 120:
            return "blocked"
        return "ok"

    def check_asymmetry(self, asymmetry: bool) -> str:
        if asymmetry:
            return "caveated"
        return "honest"
