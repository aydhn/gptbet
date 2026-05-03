from sports_signal_bot.multi_region_fabric.strategies.base import BaseMultiRegionStrategy

class FailoverGuardedStrategy(BaseMultiRegionStrategy):
    def evaluate(self) -> str:
        return "failover heavily guarded"
