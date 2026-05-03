from abc import ABC, abstractmethod

class BaseRemediationLaneStrategy(ABC):
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass
