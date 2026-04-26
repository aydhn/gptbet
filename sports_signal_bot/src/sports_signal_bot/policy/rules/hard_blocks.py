from typing import Dict, Any, List, Tuple
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord
from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule

class InvalidProbabilityRule(BasePolicyRule):
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        if signal.final_probability < 0.0 or signal.final_probability > 1.0:
            return True, [DecisionRationaleRecord(code="invalid_probability", description="Probability outside [0, 1]", impact="blocking")]
        return False, []

class MissingMarketReferenceRule(BasePolicyRule):
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        req = self.config.get("market_reference_required_for_approval", False)
        # components_summary might have it, or we assume it's in metadata. We'll use a placeholder logic.
        has_ref = signal.components_summary.get("market_implied_probability") is not None
        if req and not has_ref:
            return True, [DecisionRationaleRecord(code="missing_market_reference", description="Required market reference is missing", impact="blocking")]
        return False, []

class LowDataQualityBlockRule(BasePolicyRule):
    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        min_dq = self.config.get("hard_block_rules", {}).get("min_data_quality", 0.0)
        # Convert penalty to quality proxy: 1.0 - penalty
        quality = 1.0 - signal.components_summary.get("data_quality_penalty", 0.0)
        if quality < min_dq:
            return True, [DecisionRationaleRecord(code="too_low_data_quality", description=f"Quality {quality:.2f} < {min_dq:.2f}", impact="blocking")]
        return False, []

class HardBlockRuleSet:
    def __init__(self, config: Dict[str, Any]):
        self.rules = [
            InvalidProbabilityRule(config),
            MissingMarketReferenceRule(config),
            LowDataQualityBlockRule(config)
        ]

    def evaluate(self, signal: SignalPolicyInputRecord) -> Tuple[bool, List[DecisionRationaleRecord]]:
        all_reasons = []
        is_blocked = False
        for rule in self.rules:
            matched, reasons = rule.evaluate(signal)
            if matched:
                is_blocked = True
                all_reasons.extend(reasons)
        return is_blocked, all_reasons
