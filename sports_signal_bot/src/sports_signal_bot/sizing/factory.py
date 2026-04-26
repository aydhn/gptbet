from sports_signal_bot.sizing.contracts import SizingConfig, SizingStrategyName
from sports_signal_bot.sizing.strategies.base import BaseSizingStrategy
from sports_signal_bot.sizing.registry import SizingRegistry


class SizingFactory:
    @staticmethod
    def create(name: str, config: SizingConfig) -> BaseSizingStrategy:
        strategy_name = SizingStrategyName(name)
        strategy_class = SizingRegistry.get(strategy_name)
        return strategy_class(config)
