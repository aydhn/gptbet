from abc import ABC, abstractmethod
from typing import Tuple, List
from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord

class BaseOverlayStrategy(ABC):
    def __init__(self, config: BankrollConfig):
        self.config = config

    @abstractmethod
    def compute_stake(self, decision: BankrollDecisionRecord, current_bankroll: float) -> Tuple[float, List[str]]:
        """
        Computes the stake for a given decision.
        Returns:
            Tuple containing:
            - The calculated stake units.
            - A list of any warnings encountered during calculation.
        """
        pass

    def describe(self) -> str:
        return self.__class__.__name__
