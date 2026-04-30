from typing import List, Dict, Any, Tuple
import uuid

from .contracts import (
    CandidateReleaseRecord,
    CandidateValidationStageRecord,
    CandidateReadinessRecord,
    CandidatePromotionDecisionRecord,
    CandidateManifest,
    CandidateState
)
from .lanes import assign_lane
from .stages import build_candidate_validation_plan, run_candidate_stage_validation, detect_blocking_stage_failures
from .readiness import compute_candidate_readiness
from .decisions import build_promote_or_kill_decision

def run_candidate_pipeline(candidates: List[CandidateReleaseRecord]) -> CandidateManifest:
    """Runs the full candidate promotion pipeline for a list of candidates."""

    decisions = []
    readiness_records = []

    for candidate in candidates:
        # 1. Assign Lane
        # Simple mock metrics for gate burden and confidence
        gate_burden = "low" if candidate.risk_level == "low" else "medium"
        confidence = "high" if candidate.support_strength > 0.7 else "low"
        lane = assign_lane(candidate, gate_burden, confidence)
        candidate.lane = lane

        # 2. State transition
        candidate.current_state = CandidateState.PENDING_STAGE_VALIDATION

        # 3. Stage Validation
        plan = build_candidate_validation_plan(candidate)
        stage_results = []
        for stage in plan:
            result = run_candidate_stage_validation(candidate, stage)
            stage_results.append(result)

        blockers = detect_blocking_stage_failures(stage_results)

        if not blockers:
            candidate.current_state = CandidateState.QUALITY_GATES_PASSED
        else:
            # If safety blocked, kill
            if "safety_validation" in blockers:
                candidate.current_state = CandidateState.CANDIDATE_KILLED
            else:
                candidate.current_state = CandidateState.CANDIDATE_REVISE

        # 4. Readiness
        readiness = compute_candidate_readiness(candidate, stage_results, has_approvals=False)
        readiness_records.append(readiness)

        # 5. Promote or Kill Decision
        action, rationale = build_promote_or_kill_decision(candidate, readiness, lane)

        # 6. Final state update
        if action.value == "promote_candidate_lane":
            candidate.current_state = CandidateState.CANDIDATE_PROMOTE_RECOMMENDED
        elif action.value == "hold_candidate":
            candidate.current_state = CandidateState.CANDIDATE_HOLD
        elif action.value == "kill_candidate":
            candidate.current_state = CandidateState.CANDIDATE_KILLED
        elif action.value == "revise_candidate":
            candidate.current_state = CandidateState.CANDIDATE_REVISE

        decision = CandidatePromotionDecisionRecord(
            decision_id=str(uuid.uuid4()),
            candidate_id=candidate.candidate_release_id,
            action=action,
            rationale=rationale,
            lane=lane
        )
        decisions.append(decision)

    return CandidateManifest(
        manifest_id=str(uuid.uuid4()),
        candidates=candidates,
        decisions=decisions,
        readiness=readiness_records
    )
