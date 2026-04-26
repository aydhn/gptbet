from typing import Any, Dict

from sports_signal_bot.dynamic_weighting.contracts import \
    WeightingPolicyDefinition
from sports_signal_bot.dynamic_weighting.registry import weighting_registry
from sports_signal_bot.dynamic_weighting.strategies.base import \
    BaseWeightingStrategy


class WeightingFactory:
    @staticmethod
    def create(
        strategy_name: str, policy_data: Dict[str, Any], config: Dict[str, Any]
    ) -> BaseWeightingStrategy:
        strategy_class = weighting_registry.get(strategy_name)
        policy = WeightingPolicyDefinition(**policy_data)
        return strategy_class(policy=policy, config=config)
