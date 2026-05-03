from sports_signal_bot.multi_region_fabric.strategies.base import BaseMultiRegionStrategy

class BrokerShardStrictStrategy(BaseMultiRegionStrategy):
    def evaluate(self) -> str:
        return "shard ownership strict"
