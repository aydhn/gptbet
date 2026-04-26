from sports_signal_bot.bankroll.contracts import BankrollConfig, OverlayStrategyName
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy
from sports_signal_bot.bankroll.registry import OverlayStrategyRegistry

class OverlayFactory:
    @staticmethod
    def create(name: str, config: BankrollConfig) -> BaseOverlayStrategy:
        strategy_name = OverlayStrategyName(name)
        strategy_class = OverlayStrategyRegistry.get(strategy_name)
        return strategy_class(config)
