from .base import BaseResilienceStrategy

class GameDayFirstResilienceStrategy(BaseResilienceStrategy):
    @property
    def name(self) -> str:
        return "GameDayFirstResilienceStrategy"

    def get_relay_quarantine_multiplier(self) -> float:
        return 1.0
