from typing import Dict, Any, List, Tuple
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord
from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule

class RegimeRiskRule(BasePolicyRule):
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        # This is a placeholder for actual regime logic
        risk_penalty = signal.components_summary.get("regime_adjustment", 0.0)

        if risk_penalty < 0:
            return True, [DecisionRationaleRecord(code="supportive_regime", description="Supportive regime found", impact="positive")]
        elif risk_penalty > 0.05:
             return True, [DecisionRationaleRecord(code="risky_regime", description="Risky regime found", impact="negative")]

        return False, []
