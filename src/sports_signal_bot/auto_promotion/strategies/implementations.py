import uuid
from typing import Optional

from .base import BasePromotionStrategy
from ..contracts import (
    CandidateInputRecord,
    AutoProgressionDecisionRecord,
    AutoDecisionType,
    EligibilityStatus,
)
from ..boundaries import SafetyBoundaryEvaluator
from ..heuristics import EligibilityHeuristicsEngine
from ..evaluators import AutoDecisionEvaluator


class BalancedSemiAutonomousStrategy(BasePromotionStrategy):
    def evaluate_candidate(
        self, candidate: CandidateInputRecord, engine
    ) -> AutoProgressionDecisionRecord:
        decision_id = f"ap-{uuid.uuid4().hex[:8]}"
        warnings = []

        if decision := self._evaluate_hard_boundaries(
            candidate, decision_id
        ):
            return decision

        if decision := self._evaluate_approval_requirements(
            candidate, decision_id
        ):
            return decision

        if decision := self._evaluate_fleet_supersession(
            candidate, engine, decision_id
        ):
            return decision

        if decision := self._evaluate_auto_kill(
            candidate, engine, decision_id, warnings
        ):
            return decision

        if decision := self._evaluate_heuristics_progress(
            candidate, engine, decision_id, warnings
        ):
            return decision

        if decision := self._evaluate_auto_hold(
            candidate, engine, decision_id
        ):
            return decision

        # Default: Review Required
        score = EligibilityHeuristicsEngine.compute_heuristic_score(
            candidate, self.config
        )
        return AutoProgressionDecisionRecord(
            auto_progression_id=decision_id,
            candidate_release_id=candidate.candidate_release_id,
            current_stage=candidate.current_stage,
            proposed_next_stage=None,
            decision_type=AutoDecisionType.review_required,
            eligibility_status=EligibilityStatus.eligible_but_review_preferred,
            heuristic_score=score,
            safety_clearance_status=True,
            approval_requirement_status="none",
        )

    def _evaluate_hard_boundaries(
        self, candidate: CandidateInputRecord, decision_id: str
    ) -> Optional[AutoProgressionDecisionRecord]:
        boundaries_config = self.config.get("boundaries", {})
        blockers = SafetyBoundaryEvaluator.evaluate_hard_blocks(
            candidate, boundaries_config
        )

        if any(b.blocker_type == "manual_override" for b in blockers):
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.blocked_by_manual_override,
                eligibility_status=EligibilityStatus.blocked,
                safety_clearance_status=False,
                approval_requirement_status=candidate.approval_status,
                blockers=blockers,
            )

        if blockers:
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.blocked_by_safety,
                eligibility_status=EligibilityStatus.blocked,
                safety_clearance_status=False,
                approval_requirement_status=candidate.approval_status,
                blockers=blockers,
            )
        return None

    def _evaluate_approval_requirements(
        self, candidate: CandidateInputRecord, decision_id: str
    ) -> Optional[AutoProgressionDecisionRecord]:
        needs_approval = SafetyBoundaryEvaluator.requires_approval(candidate)
        if needs_approval and candidate.approval_status != "approved":
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.approval_required,
                eligibility_status=EligibilityStatus.approval_required,
                safety_clearance_status=True,
                approval_requirement_status="pending",
                blockers=[],
            )
        return None

    def _evaluate_fleet_supersession(
        self, candidate: CandidateInputRecord, engine, decision_id: str
    ) -> Optional[AutoProgressionDecisionRecord]:
        superseding_id = engine.supersessions.get(
            candidate.candidate_release_id
        )
        if superseding_id:
            msg = (
                f"Fleet Supersession: Replaced by stronger safer "
                f"candidate {superseding_id}"
            )
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_kill,
                eligibility_status=EligibilityStatus.kill_candidate,
                safety_clearance_status=True,
                approval_requirement_status="none",
                blockers=[],
                warnings=[msg],
            )
        return None

    def _evaluate_auto_kill(
        self,
        candidate: CandidateInputRecord,
        engine,
        decision_id: str,
        warnings: list,
    ) -> Optional[AutoProgressionDecisionRecord]:
        kill_decision = AutoDecisionEvaluator.evaluate_kill(
            candidate, self.config
        )
        if kill_decision:
            if not engine.quota.can_kill():
                warnings.append(
                    "Quota saturated for kills; executing auto-hold instead."
                )
                return AutoProgressionDecisionRecord(
                    auto_progression_id=decision_id,
                    candidate_release_id=candidate.candidate_release_id,
                    current_stage=candidate.current_stage,
                    proposed_next_stage=None,
                    decision_type=AutoDecisionType.blocked_by_capacity,
                    eligibility_status=EligibilityStatus.hold_required,
                    safety_clearance_status=False,
                    approval_requirement_status="none",
                    warnings=warnings,
                )
            engine.quota.record_kill()
            engine.kills.append(kill_decision)
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_kill,
                eligibility_status=EligibilityStatus.kill_candidate,
                safety_clearance_status=False,
                approval_requirement_status="none",
                warnings=warnings,
            )
        return None

    def _evaluate_heuristics_progress(
        self,
        candidate: CandidateInputRecord,
        engine,
        decision_id: str,
        warnings: list,
    ) -> Optional[AutoProgressionDecisionRecord]:
        score = EligibilityHeuristicsEngine.compute_heuristic_score(
            candidate, self.config
        )
        heuristics_config = self.config.get("heuristics", {})
        min_score = heuristics_config.get("minimum_progression_score", 75.0)

        if score.composite_score >= min_score:
            if not engine.quota.can_progress():
                warnings.append("Quota saturated for progress.")
                return AutoProgressionDecisionRecord(
                    auto_progression_id=decision_id,
                    candidate_release_id=candidate.candidate_release_id,
                    current_stage=candidate.current_stage,
                    proposed_next_stage=None,
                    decision_type=AutoDecisionType.blocked_by_capacity,
                    eligibility_status=EligibilityStatus.hold_required,
                    heuristic_score=score,
                    safety_clearance_status=True,
                    approval_requirement_status="none",
                    warnings=warnings,
                )

            engine.quota.record_progression()
            next_stage = self._map_next_stage(candidate.current_stage)

            status = EligibilityStatus.eligible_for_auto_progress
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=next_stage,
                decision_type=AutoDecisionType.auto_progress,
                eligibility_status=status,
                heuristic_score=score,
                safety_clearance_status=True,
                approval_requirement_status="none",
            )
        return None

    def _evaluate_auto_hold(
        self, candidate: CandidateInputRecord, engine, decision_id: str
    ) -> Optional[AutoProgressionDecisionRecord]:
        hold_decision = AutoDecisionEvaluator.evaluate_hold(
            candidate, self.config
        )
        if hold_decision:
            score = EligibilityHeuristicsEngine.compute_heuristic_score(
                candidate, self.config
            )
            engine.holds.append(hold_decision)
            return AutoProgressionDecisionRecord(
                auto_progression_id=decision_id,
                candidate_release_id=candidate.candidate_release_id,
                current_stage=candidate.current_stage,
                proposed_next_stage=None,
                decision_type=AutoDecisionType.auto_hold,
                eligibility_status=EligibilityStatus.hold_required,
                heuristic_score=score,
                safety_clearance_status=True,
                approval_requirement_status="none",
            )
        return None

    def _map_next_stage(self, current: str) -> str:
        ladder = {
            "shortlisted": "pending_stage_validation",
            "shadow_verified": "pending_candidate_eval",
            "candidate_eval_verified": "pending_live_like_safe",
            "live_like_safe_verified": "ready_for_future_release_step",
        }
        return ladder.get(current, current)
