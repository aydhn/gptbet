from .base import BaseResilienceStrategy

class SwarmStrictConsensusStrategy(BaseResilienceStrategy):
    @property
    def name(self) -> str:
        return "SwarmStrictConsensusStrategy"

    def get_relay_quarantine_multiplier(self) -> float:
        return 3.0
