from typing import Dict, Type
from sports_signal_bot.portfolio.contracts import PortfolioConfig
from sports_signal_bot.portfolio.strategies.base import BaseAllocationStrategy
from sports_signal_bot.portfolio.strategies.sequential_cap import SequentialCapAllocation
from sports_signal_bot.portfolio.strategies.proportional_priority import ProportionalPriorityAllocation
from sports_signal_bot.portfolio.strategies.tiered_action_class import TieredActionClassAllocation
from sports_signal_bot.portfolio.strategies.conservative_exposure import ConservativeExposureAllocation
from sports_signal_bot.portfolio.strategies.budget_reserve import BudgetReserveAllocation
from sports_signal_bot.portfolio.strategies.shadow_no_allocation import ShadowNoAllocation

class PortfolioStrategyFactory:
    _registry: Dict[str, Type[BaseAllocationStrategy]] = {
        "sequential_cap": SequentialCapAllocation,
        "proportional_priority": ProportionalPriorityAllocation,
        "tiered_action_class": TieredActionClassAllocation,
        "conservative_exposure": ConservativeExposureAllocation,
        "budget_reserve": BudgetReserveAllocation,
        "shadow_no_allocation": ShadowNoAllocation,
    }

    @classmethod
    def create(cls, strategy_name: str, config: PortfolioConfig) -> BaseAllocationStrategy:
        if strategy_name not in cls._registry:
            raise ValueError(f"Unknown portfolio strategy: {strategy_name}")
        return cls._registry[strategy_name](config)
