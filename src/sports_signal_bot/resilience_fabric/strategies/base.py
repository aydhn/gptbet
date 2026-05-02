from abc import ABC, abstractmethod

class BaseResilienceStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_relay_quarantine_multiplier(self) -> float:
        pass
