from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseConcurrencyHardeningStrategy(ABC):
    """Base class for concurrency hardening strategies."""

    @abstractmethod
    def get_max_parallelism(self) -> int:
        pass

    @abstractmethod
    def get_stale_read_tolerance_ms(self) -> int:
        pass

    @abstractmethod
    def is_race_release_blocking(self) -> bool:
        pass

    @abstractmethod
    def requires_strict_idempotency(self) -> bool:
        pass

class ConservativeConcurrencyHardeningStrategy(BaseConcurrencyHardeningStrategy):
    """Conservative strategy with strict safety guarantees."""

    def get_max_parallelism(self) -> int:
        return 4

    def get_stale_read_tolerance_ms(self) -> int:
        return 0 # Zero tolerance

    def is_race_release_blocking(self) -> bool:
        return True # Any race blocks release

    def requires_strict_idempotency(self) -> bool:
        return True
