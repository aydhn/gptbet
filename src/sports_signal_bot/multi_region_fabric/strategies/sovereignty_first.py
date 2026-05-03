from sports_signal_bot.multi_region_fabric.strategies.base import BaseMultiRegionStrategy

class SovereigntyFirstRemediationStrategy(BaseMultiRegionStrategy):
    def evaluate(self) -> str:
        return "sovereignty constraints heavy"
