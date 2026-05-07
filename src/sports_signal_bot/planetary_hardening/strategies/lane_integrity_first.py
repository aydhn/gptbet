from .base import BasePlanetaryHardeningStrategy

class LaneIntegrityFirstStrategy(BasePlanetaryHardeningStrategy):
    @property
    def name(self) -> str:
        return "LaneIntegrityFirstStrategy"

    @property
    def reject_stale(self) -> bool:
        return True

    @property
    def require_replayable_handoffs(self) -> bool:
        return False
