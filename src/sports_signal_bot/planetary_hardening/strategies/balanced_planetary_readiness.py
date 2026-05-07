from .base import BasePlanetaryHardeningStrategy

class BalancedPlanetaryReadinessStrategy(BasePlanetaryHardeningStrategy):
    @property
    def name(self) -> str:
        return "BalancedPlanetaryReadinessStrategy"

    @property
    def reject_stale(self) -> bool:
        return False

    @property
    def require_replayable_handoffs(self) -> bool:
        return True
