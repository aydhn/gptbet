from typing import Any, Dict, List, Tuple

from sports_signal_bot.policy.contracts import DecisionRationaleRecord
from sports_signal_bot.policy.rules.base import BasePolicyRule
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord


class WatchlistScoreRule(BasePolicyRule):
    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        min_w = self.config.get("score_bands", {}).get("no_bet", 0.4)
        if signal.final_signal_score >= min_w:
            return True, [
                DecisionRationaleRecord(
                    code="watchlist_score",
                    description=f"Score {signal.final_signal_score:.2f} >= watchlist min {min_w}",
                    impact="neutral",
                )
            ]
        return False, []


class WatchlistRuleSet:
    def __init__(self, config: Dict[str, Any]):
        self.rules = [WatchlistScoreRule(config)]

    def evaluate(
        self, signal: SignalPolicyInputRecord
    ) -> Tuple[bool, List[DecisionRationaleRecord]]:
        all_reasons = []
        is_watchlist = True
        for rule in self.rules:
            matched, reasons = rule.evaluate(signal)
            if not matched:
                is_watchlist = False
                break
            all_reasons.extend(reasons)
        return is_watchlist, all_reasons
