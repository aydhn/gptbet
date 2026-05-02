from .base import BaseResilienceStrategy

class ConservativeResilienceStrategy(BaseResilienceStrategy):
    @property
    def name(self) -> str:
        return "ConservativeResilienceStrategy"

    def get_relay_quarantine_multiplier(self) -> float:
        return 2.0 # Double quarantine time
