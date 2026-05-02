from .base import BaseResilienceStrategy

class CalibrationGuardedStrategy(BaseResilienceStrategy):
    @property
    def name(self) -> str:
        return "CalibrationGuardedStrategy"

    def get_relay_quarantine_multiplier(self) -> float:
        return 1.5
