import uuid
from typing import Dict, Any
from .base import BasePromotionStrategy
from ..contracts import CandidateInputRecord, AutoProgressionDecisionRecord, AutoDecisionType, EligibilityStatus
from ..boundaries import SafetyBoundaryEvaluator
from ..heuristics import EligibilityHeuristicsEngine
from ..evaluators import AutoDecisionEvaluator

class BalancedSemiAutonomousStrategy(BasePromotionStrategy):
    def evaluate_candidate(self, candidate: CandidateInputRecord, engine) -> AutoProgressionDecisionRecord:
        decision_id = f"ap-{uuid.uuid4().hex[:8]}"
        warnings = []

        # 1. Hard Boundaries (Manuel override / safety block)
        blockers = SafetyBoundaryEvaluator.evaluate_hard_blocks(candidate, self.config.get("boundaries", {}))

        if any(b.blocker_type == "manual_override" for b in blockers):
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.blocked_by_manual_override,
                eligibility_status=EligibilityStatus.blocked, safety_clearance_status=False,
                approval_requirement_status=candidate.approval_status, blockers=blockers
            )

        if blockers:
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.blocked_by_safety,
                eligibility_status=EligibilityStatus.blocked, safety_clearance_status=False,
                approval_requirement_status=candidate.approval_status, blockers=blockers
            )

        # 2. Approval Requirement
        if SafetyBoundaryEvaluator.requires_approval(candidate) and candidate.approval_status != "approved":
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.approval_required,
                eligibility_status=EligibilityStatus.approval_required, safety_clearance_status=True,
                approval_requirement_status="pending", blockers=[]
            )

        # 3. Fleet Supersession Engine
        superseding_id = engine.supersessions.get(candidate.candidate_release_id)
        if superseding_id:
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_kill,
                eligibility_status=EligibilityStatus.kill_candidate, safety_clearance_status=True,
                approval_requirement_status="none", blockers=[],
                warnings=[f"Fleet Supersession: Replaced by stronger safer candidate {superseding_id}"]
            )

        # 4. Auto Kill Evaluator
        kill_decision = AutoDecisionEvaluator.evaluate_kill(candidate, self.config)
        if kill_decision:
            if not engine.quota.can_kill():
                warnings.append("Quota saturated for kills; executing auto-hold instead.")
                return AutoProgressionDecisionRecord(
                    auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                    current_stage=candidate.current_stage, proposed_next_stage=None,
                    decision_type=AutoDecisionType.blocked_by_capacity,
                    eligibility_status=EligibilityStatus.hold_required, safety_clearance_status=False,
                    approval_requirement_status="none", warnings=warnings
                )
            engine.quota.record_kill()
            engine.kills.append(kill_decision)
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_kill,
                eligibility_status=EligibilityStatus.kill_candidate, safety_clearance_status=False,
                approval_requirement_status="none", warnings=warnings
            )

        # 5. Heuristics & Auto-Progress
        score = EligibilityHeuristicsEngine.compute_heuristic_score(candidate, self.config)
        min_score = self.config.get("heuristics", {}).get("minimum_progression_score", 75.0)

        if score.composite_score >= min_score:
            if not engine.quota.can_progress():
                return AutoProgressionDecisionRecord(
                    auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                    current_stage=candidate.current_stage, proposed_next_stage=None,
                    decision_type=AutoDecisionType.blocked_by_capacity,
                    eligibility_status=EligibilityStatus.hold_required, heuristic_score=score,
                    safety_clearance_status=True, approval_requirement_status="none",
                    warnings=["Quota saturated for progress."]
                )

            engine.quota.record_progression()
            next_stage = self._map_next_stage(candidate.current_stage)

            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=next_stage,
                decision_type=AutoDecisionType.auto_progress,
                eligibility_status=EligibilityStatus.eligible_for_auto_progress, heuristic_score=score,
                safety_clearance_status=True, approval_requirement_status="none"
            )

        # 6. Auto Hold Evaluator
        hold_decision = AutoDecisionEvaluator.evaluate_hold(candidate, self.config)
        if hold_decision:
            engine.holds.append(hold_decision)
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage, proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_hold,
                eligibility_status=EligibilityStatus.hold_required, heuristic_score=score,
                safety_clearance_status=True, approval_requirement_status="none"
            )

        # Default: Review Required
        return AutoProgressionDecisionRecord(
            auto_progression_id=decision_id, candidate_release_id=candidate.candidate_release_id,
            current_stage=candidate.current_stage, proposed_next_stage=None,
            decision_type=AutoDecisionType.review_required,
            eligibility_status=EligibilityStatus.eligible_but_review_preferred, heuristic_score=score,
            safety_clearance_status=True, approval_requirement_status="none"
        )

    def _map_next_stage(self, current: str) -> str:
        ladder = {
            "shortlisted": "pending_stage_validation",
            "shadow_verified": "pending_candidate_eval",
            "candidate_eval_verified": "pending_live_like_safe",
            "live_like_safe_verified": "ready_for_future_release_step"
        }
        return ladder.get(current, current)
