from typing import Any, Dict, List, Tuple

from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord


class ScoreGrayZoneRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        rules = self.config.get("no_bet_zone_rules", {})
        min_s = rules.get("min_score", 0.0)
        max_s = rules.get("max_score", 0.0)

        if min_s <= signal.final_signal_score < max_s:
            return True, [
                DecisionRationaleRecord(
                    code="no_bet_gray_zone",
                    description=f"Score {signal.final_signal_score:.2f} in gray zone [{min_s}, {max_s})",
                    impact="negative",
                )
            ]
        return False, []


class HighUncertaintyRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        max_u = self.config.get("uncertainty_limits", {}).get("max_acceptable", 1.0)
        u = signal.components_summary.get("uncertainty_penalty", 0.0)
        if u > max_u:
            return True, [
                DecisionRationaleRecord(
                    code="high_uncertainty",
                    description=f"Uncertainty {u:.2f} > {max_u}",
                    impact="negative",
                )
            ]
        return False, []


class HighDisagreementRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        max_d = self.config.get("disagreement_limits", {}).get("max_acceptable", 1.0)
        d = signal.components_summary.get("disagreement_penalty", 0.0)
        if d > max_d:
            return True, [
                DecisionRationaleRecord(
                    code="high_disagreement",
                    description=f"Disagreement {d:.2f} > {max_d}",
                    impact="negative",
                )
            ]
        return False, []


class InsufficientEdgeRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        min_edge = self.config.get("edge_bands", {}).get("low", 0.01)
        if signal.edge_estimate < min_edge:
            return True, [
                DecisionRationaleRecord(
                    code="insufficient_edge",
                    description=f"Edge {signal.edge_estimate:.3f} < {min_edge}",
                    impact="negative",
                )
            ]
        return False, []


class NoBetRuleSet:
    def __init__(self, config: Dict[str, Any]):
        self.rules = [
            ScoreGrayZoneRule(config),
            HighUncertaintyRule(config),
            HighDisagreementRule(config),
            InsufficientEdgeRule(config),
        ]

    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        all_reasons = []
        is_no_bet = False
        for rule in self.rules:
            matched, reasons = rule.evaluate(signal)
            if matched:
                is_no_bet = True
                all_reasons.extend(reasons)
        return is_no_bet, all_reasons
