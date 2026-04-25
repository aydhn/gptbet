from typing import Dict, Type
from sports_signal_bot.dynamic_weighting.strategies.base import BaseWeightingStrategy
from sports_signal_bot.dynamic_weighting.strategies.static_policy import StaticPolicyWeighted
from sports_signal_bot.dynamic_weighting.strategies.trust_weighted import TrustWeighted
from sports_signal_bot.dynamic_weighting.strategies.regime_aware import RegimeAwareWeighted
from sports_signal_bot.dynamic_weighting.strategies.conservative_disagreement import ConservativeDisagreementWeighted
from sports_signal_bot.dynamic_weighting.strategies.dynamic_hybrid import DynamicHybridWeighted
from sports_signal_bot.dynamic_weighting.strategies.single_best import SingleBestSourceWeighted

class WeightingRegistry:
    def __init__(self):
        self._strategies: Dict[str, Type[BaseWeightingStrategy]] = {
            'static_policy': StaticPolicyWeighted,
            'trust_weighted': TrustWeighted,
            'regime_aware': RegimeAwareWeighted,
            'conservative_disagreement': ConservativeDisagreementWeighted,
            'dynamic_hybrid': DynamicHybridWeighted,
            'single_best': SingleBestSourceWeighted,
        }

    def register(self, name: str, strategy_class: Type[BaseWeightingStrategy]):
        self._strategies[name] = strategy_class

    def get(self, name: str) -> Type[BaseWeightingStrategy]:
        if name not in self._strategies:
            raise ValueError(f"Unknown weighting strategy: {name}")
        return self._strategies[name]

    def list_strategies(self) -> list:
        return list(self._strategies.keys())

# Global registry
weighting_registry = WeightingRegistry()
