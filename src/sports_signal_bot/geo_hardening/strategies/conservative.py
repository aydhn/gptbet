from typing import Any, Dict

from .base import BaseGeoStrategy


class ConservativeGeoHardeningStrategy(BaseGeoStrategy):
    def check_lag(self, lag: int) -> str:
        if lag > 0:
            return "blocked"
        return "ok"

    def check_asymmetry(self, asymmetry: bool) -> str:
        if asymmetry:
            return "blocked"
        return "honest"
