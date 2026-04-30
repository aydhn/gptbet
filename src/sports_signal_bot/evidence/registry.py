from typing import Dict, Type
from sports_signal_bot.evidence.strategies.base import BaseExplainabilityStrategy
from sports_signal_bot.evidence.strategies.conservative_audit import ConservativeAuditStrategy
from sports_signal_bot.evidence.strategies.operator_concise import OperatorConciseStrategy
from sports_signal_bot.evidence.strategies.balanced_review import BalancedReviewStrategy

class StrategyRegistry:
    def __init__(self):
        self._strategies: Dict[str, Type[BaseExplainabilityStrategy]] = {
            "conservative_audit": ConservativeAuditStrategy,
            "operator_concise": OperatorConciseStrategy,
            "balanced_review": BalancedReviewStrategy
        }

    def get_strategy(self, name: str) -> BaseExplainabilityStrategy:
        strategy_cls = self._strategies.get(name)
        if not strategy_cls:
            raise ValueError(f"Strategy {name} not found")
        return strategy_cls()

    def list_strategies(self):
        return list(self._strategies.keys())
