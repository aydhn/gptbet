from abc import ABC, abstractmethod

class BasePlanetaryHardeningStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def reject_stale(self) -> bool:
        pass

    @property
    @abstractmethod
    def require_replayable_handoffs(self) -> bool:
        pass
