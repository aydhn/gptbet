from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord
from sports_signal_bot.policy.contracts import DecisionRationaleRecord

class BasePolicyRule(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        """
        Evaluate the rule against a signal.
        Returns a tuple of (rule_matched, list of rationale records).
        If the rule implies a block or no-bet, rule_matched=True means the block/no-bet is active.
        """
        pass

    def explain(self) -> str:
        return self.__class__.__name__
