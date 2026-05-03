from sports_signal_bot.multi_region_fabric.strategies.base import BaseMultiRegionStrategy

class ConservativeMultiRegionFabricStrategy(BaseMultiRegionStrategy):
    def evaluate(self) -> str:
        return "local-first, failover cautious"
