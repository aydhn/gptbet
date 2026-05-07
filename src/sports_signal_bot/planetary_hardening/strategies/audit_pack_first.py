from .base import BasePlanetaryHardeningStrategy

class AuditPackFirstStrategy(BasePlanetaryHardeningStrategy):
    @property
    def name(self) -> str:
        return "AuditPackFirstStrategy"

    @property
    def reject_stale(self) -> bool:
        return True

    @property
    def require_replayable_handoffs(self) -> bool:
        return True
