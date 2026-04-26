from typing import Dict, Any, List
import uuid
from sports_signal_bot.signal_scoring.contracts import SignalPolicyInputRecord
from sports_signal_bot.policy.contracts import (
    PolicyDecisionRecord, PolicySignalStatus, ActionClass,
    DecisionRationaleRecord, PolicyManifest, PolicyLifecycleRecord
)
from sports_signal_bot.policy.factory import PolicyStrategyFactory

class PolicyRunner:
    def __init__(self, config: Dict[str, Any], strategy_name: str = "balanced"):
        self.config = config
        self.strategy = PolicyStrategyFactory.build(strategy_name, config)
        self.action_mapping = self.config.get("action_class_mapping", {})

    def evaluate_signal(self, signal: SignalPolicyInputRecord) -> PolicyDecisionRecord:
        rationales: List[DecisionRationaleRecord] = []

        # 1. Hard Blocks
        is_blocked, hr_reasons = self.strategy["hard_blocks"].evaluate(signal)
        if is_blocked:
            rationales.extend(hr_reasons)
            return self._build_decision(signal, PolicySignalStatus.BLOCKED, rationales, hr_reasons)

        # Extras (like regime risk)
        for extra_rule in self.strategy.get("extras", []):
            matched, ex_reasons = extra_rule.evaluate(signal)
            if matched:
                rationales.extend(ex_reasons)

        # Check if extras force a block
        if any(r.impact == "blocking" for r in rationales):
            return self._build_decision(signal, PolicySignalStatus.BLOCKED, rationales, [r for r in rationales if r.impact == "blocking"])

        # 2. No Bet Zone
        is_no_bet, nb_reasons = self.strategy["no_bet"].evaluate(signal)
        if is_no_bet:
            rationales.extend(nb_reasons)
            # If it's a weak signal, maybe classify as such
            if signal.final_signal_score < self.config.get("score_bands", {}).get("no_bet", 0.4):
                return self._build_decision(signal, PolicySignalStatus.WEAK_SIGNAL, rationales, nb_reasons)
            return self._build_decision(signal, PolicySignalStatus.NO_BET_ZONE, rationales, nb_reasons)

        # 3. Watchlist
        is_watchlist, w_reasons = self.strategy["watchlist"].evaluate(signal)
        # Note: watchlist implies it's not candidate yet.

        # 4. Candidate
        is_candidate, c_reasons = self.strategy["candidate"].evaluate(signal)

        if is_candidate:
            rationales.extend(c_reasons)
            # 5. Approval
            is_approved, a_reasons = self.strategy["approval"].evaluate(signal)
            if is_approved:
                rationales.extend(a_reasons)
                return self._build_decision(signal, PolicySignalStatus.APPROVED, rationales, [])
            else:
                return self._build_decision(signal, PolicySignalStatus.CANDIDATE, rationales, [])

        if is_watchlist:
            rationales.extend(w_reasons)
            return self._build_decision(signal, PolicySignalStatus.BELOW_THRESHOLD, rationales, [])

        # Fallback
        return self._build_decision(signal, PolicySignalStatus.PENDING, rationales, [])

    def _build_decision(self, signal: SignalPolicyInputRecord, status: PolicySignalStatus,
                       all_rationales: List[DecisionRationaleRecord],
                       blocking_or_no_bet_reasons: List[DecisionRationaleRecord]) -> PolicyDecisionRecord:

        action = self.action_mapping.get(status.value, ActionClass.NO_ACTION)

        return PolicyDecisionRecord(
            event_id=signal.event_id,
            sport=signal.sport,
            market_type=signal.market_type,
            selection=signal.selection,
            signal_status=status,
            action_class=ActionClass(action),
            decision_score=signal.final_signal_score,
            policy_name=self.strategy["name"],
            rationale_codes=[r.code for r in all_rationales],
            no_bet_reasons=[r.code for r in blocking_or_no_bet_reasons if r.impact == "negative"],
            block_reasons=[r.code for r in blocking_or_no_bet_reasons if r.impact == "blocking"],
            warnings=[]
        )

    def run(self, signals: List[SignalPolicyInputRecord], sport: str, market: str) -> PolicyManifest:
        decisions = []
        lifecycles = []

        for sig in signals:
            decision = self.evaluate_signal(sig)
            decisions.append(decision)

            lifecycles.append(PolicyLifecycleRecord(
                event_id=sig.event_id,
                sport=sig.sport,
                market_type=sig.market_type,
                selection=sig.selection,
                previous_status=PolicySignalStatus.SCORED,
                new_status=decision.signal_status,
                transition_reason="Policy evaluation"
            ))

        # Build Manifest
        manifest = PolicyManifest(
            run_id=str(uuid.uuid4()),
            sport=sport,
            market_type=market,
            policy_name=self.strategy["name"],
            total_evaluated=len(signals),
            decisions=decisions,
            lifecycle_events=lifecycles
        )

        for d in decisions:
            if d.signal_status == PolicySignalStatus.APPROVED: manifest.approved_count += 1
            elif d.signal_status == PolicySignalStatus.CANDIDATE: manifest.candidate_count += 1
            elif d.action_class == ActionClass.WATCHLIST: manifest.watchlist_count += 1
            elif d.signal_status == PolicySignalStatus.BLOCKED: manifest.blocked_count += 1
            elif d.action_class == ActionClass.NO_ACTION: manifest.no_action_count += 1

            for code in d.rationale_codes:
                manifest.top_rationale_codes[code] = manifest.top_rationale_codes.get(code, 0) + 1
            for code in d.no_bet_reasons:
                manifest.no_bet_zone_reasons[code] = manifest.no_bet_zone_reasons.get(code, 0) + 1
            for code in d.block_reasons:
                manifest.blocked_reasons[code] = manifest.blocked_reasons.get(code, 0) + 1

        return manifest
