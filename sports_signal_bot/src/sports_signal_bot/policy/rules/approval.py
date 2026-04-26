from typing import Any, Dict, List, Tuple

from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord


class StrongScoreRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        reqs = self.config.get("approval_requirements", {})
        min_s = reqs.get("min_score", 0.8)
        if signal.final_signal_score >= min_s:
            return True, [
                DecisionRationaleRecord(
                    code="passed_score_threshold",
                    description=f"Score {signal.final_signal_score:.2f} >= {min_s}",
                    impact="positive",
                )
            ]
        return False, []


class StrongEdgeRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        reqs = self.config.get("approval_requirements", {})
        min_e = reqs.get("min_edge", 0.03)
        if signal.edge_estimate >= min_e:
            return True, [
                DecisionRationaleRecord(
                    code="passed_edge_threshold",
                    description=f"Edge {signal.edge_estimate:.3f} >= {min_e}",
                    impact="positive",
                )
            ]
        return False, []


class LowUncertaintyRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        reqs = self.config.get("approval_requirements", {})
        max_u = reqs.get("max_uncertainty", 0.1)
        u = signal.components_summary.get("uncertainty_penalty", 0.0)
        if u <= max_u:
            return True, [
                DecisionRationaleRecord(
                    code="low_uncertainty",
                    description=f"Uncertainty {u:.2f} <= {max_u}",
                    impact="positive",
                )
            ]
        return False, []


class LowDisagreementRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        reqs = self.config.get("approval_requirements", {})
        max_d = reqs.get("max_disagreement", 0.2)
        d = signal.components_summary.get("disagreement_penalty", 0.0)
        if d <= max_d:
            return True, [
                DecisionRationaleRecord(
                    code="low_disagreement",
                    description=f"Disagreement {d:.2f} <= {max_d}",
                    impact="positive",
                )
            ]
        return False, []


class ApprovalRuleSet:
    def __init__(self, config: Dict[str, Any]):
        self.rules = [
            StrongScoreRule(config),
            StrongEdgeRule(config),
            LowUncertaintyRule(config),
            LowDisagreementRule(config),
        ]

    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        # All must match for approval
        all_reasons = []
        is_approved = True
        for rule in self.rules:
            matched, reasons = rule.evaluate(signal)
            if not matched:
                is_approved = False
                break
            all_reasons.extend(reasons)

        if is_approved:
            all_reasons.append(
                DecisionRationaleRecord(
                    code="approved_by_strong_signal",
                    description="All approval conditions met",
                    impact="positive",
                )
            )
            return True, all_reasons
        return False, []
