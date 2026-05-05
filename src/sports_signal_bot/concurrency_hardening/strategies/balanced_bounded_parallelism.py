from .base import BaseConcurrencyHardeningStrategy

class BalancedBoundedParallelismStrategy(BaseConcurrencyHardeningStrategy):
    """Balanced strategy for bounded parallelism with reasonable throughput."""

    def get_max_parallelism(self) -> int:
        return 16

    def get_stale_read_tolerance_ms(self) -> int:
        return 500 # 500ms tolerance for non-critical reads

    def is_race_release_blocking(self) -> bool:
        return True # Races still block

    def requires_strict_idempotency(self) -> bool:
        return True
