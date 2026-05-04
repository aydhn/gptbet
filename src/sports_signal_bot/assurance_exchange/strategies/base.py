from abc import ABC, abstractmethod

class BaseAssuranceExchangeStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply_currentness_rules(self, snapshot_age: int) -> str:
        pass

    @abstractmethod
    def apply_board_clearing_rules(self) -> str:
        pass
