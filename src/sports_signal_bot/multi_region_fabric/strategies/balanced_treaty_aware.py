from sports_signal_bot.multi_region_fabric.strategies.base import BaseMultiRegionStrategy

class BalancedTreatyAwareFabricStrategy(BaseMultiRegionStrategy):
    def evaluate(self) -> str:
        return "balanced, treaty-bound assistance"
