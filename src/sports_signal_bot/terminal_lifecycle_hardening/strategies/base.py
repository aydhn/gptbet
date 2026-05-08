from abc import ABC, abstractmethod

class BaseTerminalLifecycleStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, integrator) -> dict:
        pass
