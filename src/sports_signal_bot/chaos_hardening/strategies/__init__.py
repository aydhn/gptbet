from .base import BaseChaosHardeningStrategy
from .conservative import ConservativeChaosHardeningStrategy
from .balanced_fault_tolerance import BalancedFaultToleranceStrategy
from .recovery_honesty_first import RecoveryHonestyFirstStrategy
from .degradation_visibility_first import DegradationVisibilityFirstStrategy

STRATEGY_REGISTRY = {
    "conservative": ConservativeChaosHardeningStrategy,
    "balanced_fault_tolerance": BalancedFaultToleranceStrategy,
    "recovery_honesty_first": RecoveryHonestyFirstStrategy,
    "degradation_visibility_first": DegradationVisibilityFirstStrategy
}
