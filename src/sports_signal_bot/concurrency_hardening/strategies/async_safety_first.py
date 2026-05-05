from .base import BaseConcurrencyHardeningStrategy

class AsyncSafetyFirstStrategy(BaseConcurrencyHardeningStrategy):
    """Strategy prioritizing async ordering, cancellation safety, and shared state."""

    def get_max_parallelism(self) -> int:
        return 8

    def get_stale_read_tolerance_ms(self) -> int:
        return 100 # Tight drift window

    def is_race_release_blocking(self) -> bool:
        return True

    def requires_strict_idempotency(self) -> bool:
        return True
