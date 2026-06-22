from typing import Any, Dict

from .base import BaseGeoStrategy


class SymmetryFirstStrategy(BaseGeoStrategy):
    def check_lag(self, lag: int) -> str:
        if lag > 30:
            return "caveated"
        return "ok"

    def check_asymmetry(self, asymmetry: bool) -> str:
        if asymmetry:
            return "blocked"
        return "honest"
