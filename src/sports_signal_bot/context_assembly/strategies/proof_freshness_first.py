from .base import BaseContextAssemblyStrategy
from ..freshness_cases import CASE_REVIEW_ONLY

class ProofFreshnessFirstStrategy(BaseContextAssemblyStrategy):
    """
    proof freshness, refresh evidence ve trace applicability baskın
    weak freshness hızla review_only/no_safe olur
    council caps daha görünür olur
    """
    def apply_freshness_rules(self, case):
        if case.escalation_state == "none":
            case.case_status = CASE_REVIEW_ONLY
