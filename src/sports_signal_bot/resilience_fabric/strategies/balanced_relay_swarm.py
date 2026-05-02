from .base import BaseResilienceStrategy

class BalancedRelaySwarmStrategy(BaseResilienceStrategy):
    @property
    def name(self) -> str:
        return "BalancedRelaySwarmStrategy"

    def get_relay_quarantine_multiplier(self) -> float:
        return 1.0
