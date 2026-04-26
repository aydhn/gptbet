from typing import Dict, Any, List, Tuple
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord
from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule

class CandidateScoreRule(BasePolicyRule):
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        min_c = self.config.get("score_bands", {}).get("watchlist", 0.6)  # Just above watchlist
        if signal.final_signal_score >= min_c:
            return True, [DecisionRationaleRecord(code="candidate_score", description=f"Score {signal.final_signal_score:.2f} >= candidate min {min_c}", impact="positive")]
        return False, []

class CandidateRuleSet:
    def __init__(self, config: Dict[str, Any]):
        self.rules = [CandidateScoreRule(config)]

    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        all_reasons = []
        is_candidate = True
        for rule in self.rules:
            matched, reasons = rule.evaluate(signal)
            if not matched:
                is_candidate = False
                break
            all_reasons.extend(reasons)

        if is_candidate:
            all_reasons.append(DecisionRationaleRecord(code="candidate_but_not_approved", description="Candidate conditions met but lacking strong approval", impact="neutral"))
            return True, all_reasons
        return False, []
