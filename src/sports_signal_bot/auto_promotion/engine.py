import json
from typing import List, Dict, Any
from .contracts import (
    CandidateInputRecord, AutoProgressionDecisionRecord,
    AutoKillDecisionRecord, AutoHoldDecisionRecord, AutoPromotionSummaryRecord,
    AutoDecisionType
)
from .quotas import QuotaManager
from .fleet import FleetAwarenessEngine
from .strategies.implementations import BalancedSemiAutonomousStrategy

class AutoPromotionEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.quota = QuotaManager(config)
        self.strategy = BalancedSemiAutonomousStrategy(config)

        self.supersessions = {}
        self.kills: List[AutoKillDecisionRecord] = []
        self.holds: List[AutoHoldDecisionRecord] = []
        self.decisions: List[AutoProgressionDecisionRecord] = []

    def run_pass(self, candidates: List[CandidateInputRecord]) -> AutoPromotionSummaryRecord:
        self.supersessions = FleetAwarenessEngine.detect_supersessions(candidates)

        for candidate in candidates:
            decision = self.strategy.evaluate_candidate(candidate, self)
            self.decisions.append(decision)

        summary = self._generate_summary(candidates)
        self._export_artifacts(summary)
        return summary

    def _generate_summary(self, candidates: List[CandidateInputRecord]) -> AutoPromotionSummaryRecord:
        return AutoPromotionSummaryRecord(
            total_evaluated=len(candidates),
            eligible_for_auto_progress_count=sum(1 for d in self.decisions if d.decision_type == AutoDecisionType.auto_progress),
            auto_progress_count=self.quota.quota.used_progressions,
            auto_hold_count=len(self.holds),
            auto_kill_count=len(self.kills),
            review_required_count=sum(1 for d in self.decisions if d.decision_type in (AutoDecisionType.review_required, AutoDecisionType.approval_required)),
            safety_boundary_block_count=sum(1 for d in self.decisions if d.decision_type == AutoDecisionType.blocked_by_safety),
            quota_block_count=sum(1 for d in self.decisions if d.decision_type == AutoDecisionType.blocked_by_capacity),
            fleet_suppression_count=len(self.supersessions),
            future_release_step_ready_count=sum(1 for d in self.decisions if d.proposed_next_stage == "ready_for_future_release_step")
        )

    def _export_artifacts(self, summary: AutoPromotionSummaryRecord):
        with open("auto_progression_decisions.json", "w") as f:
            json.dump([d.model_dump() for d in self.decisions], f, indent=2, default=str)
        if self.kills:
            with open("auto_kill_decisions.json", "w") as f:
                json.dump([k.model_dump() for k in self.kills], f, indent=2, default=str)
        if self.holds:
            with open("auto_hold_decisions.json", "w") as f:
                json.dump([h.model_dump() for h in self.holds], f, indent=2, default=str)

        with open("auto_promotion_summary.json", "w") as f:
            f.write(summary.model_dump_json(indent=2))
