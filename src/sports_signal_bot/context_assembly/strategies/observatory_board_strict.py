from .base import BaseContextAssemblyStrategy
from ..board_cases import CASE_BLOCKED

class ObservatoryBoardStrictStrategy(BaseContextAssemblyStrategy):
    """
    degraded or stale exchanges hızla düşer
    signal freshness ve alert integrity çok sıkı
    """
    def apply_exchange_rules(self, case):
        if case.escalation_state == "none":
             case.case_status = CASE_BLOCKED
