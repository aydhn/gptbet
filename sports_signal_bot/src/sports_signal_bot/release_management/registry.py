from typing import Dict, Type

from sports_signal_bot.release_management.strategies.base import ReleaseStrategy
from sports_signal_bot.release_management.strategies.conservative_promotion import ConservativePromotionStrategy
from sports_signal_bot.release_management.strategies.direct_promotion_placeholder import DirectPromotionStrategy
from sports_signal_bot.release_management.strategies.emergency_rollback import EmergencyRollbackStrategy
from sports_signal_bot.release_management.strategies.slot_aware_canary import SlotAwareCanaryStrategy
from sports_signal_bot.release_management.strategies.stable_first_recovery import StableFirstRecoveryStrategy


class StrategyRegistry:
    _strategies: Dict[str, Type[ReleaseStrategy]] = {
        "conservative_promotion": ConservativePromotionStrategy,
        "stable_first_recovery": StableFirstRecoveryStrategy,
        "slot_aware_canary": SlotAwareCanaryStrategy,
        "emergency_rollback": EmergencyRollbackStrategy,
        "direct_promotion_placeholder": DirectPromotionStrategy,
    }

    @classmethod
    def get_strategy(cls, name: str) -> ReleaseStrategy:
        strategy_class = cls._strategies.get(name, ConservativePromotionStrategy)
        return strategy_class()

    @classmethod
    def list_strategies(cls) -> list[str]:
        return list(cls._strategies.keys())
