import uuid
from typing import Dict, Any, List
from .contracts import CouncilVoteLikeRecord, CouncilDecisionType

def evaluate_safety_lens(context: Dict[str, Any]) -> CouncilVoteLikeRecord:
    blockers = []
    notes = []
    recommendation = CouncilDecisionType.APPROVE_HANDOFF

    if context.get("risk_level", "low") == "high" and not context.get("rollback_ready", False):
        blockers.append("High risk without rollback procedure.")
        recommendation = CouncilDecisionType.REJECT_HANDOFF

    if context.get("unresolved_disputes", 0) > 0:
        notes.append("Has unresolved disputes.")
        recommendation = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

    return CouncilVoteLikeRecord(
        vote_id=str(uuid.uuid4()),
        lens_name="safety_lens",
        recommendation=recommendation,
        blockers=blockers,
        notes=notes
    )

def evaluate_evidence_lens(context: Dict[str, Any]) -> CouncilVoteLikeRecord:
    blockers = []
    notes = []
    recommendation = CouncilDecisionType.APPROVE_HANDOFF

    evidence_score = context.get("evidence_score", 0.0)
    if evidence_score < 0.6:
        blockers.append("Evidence completeness is too low.")
        recommendation = CouncilDecisionType.REJECT_HANDOFF
    elif evidence_score < 0.8:
        notes.append("Evidence is weak, recommending hold.")
        recommendation = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

    return CouncilVoteLikeRecord(
        vote_id=str(uuid.uuid4()),
        lens_name="evidence_lens",
        recommendation=recommendation,
        blockers=blockers,
        notes=notes
    )

def evaluate_simulation_lens(context: Dict[str, Any]) -> CouncilVoteLikeRecord:
    blockers = []
    notes = []
    recommendation = CouncilDecisionType.APPROVE_HANDOFF

    sim_score = context.get("simulation_score", 0.0)
    if sim_score < 0.7:
        blockers.append("Simulation results are failing.")
        recommendation = CouncilDecisionType.REJECT_HANDOFF
    elif context.get("stale_simulation", False):
        notes.append("Simulation data is stale.")
        recommendation = CouncilDecisionType.REQUIRE_ADDITIONAL_SIMULATION

    return CouncilVoteLikeRecord(
        vote_id=str(uuid.uuid4()),
        lens_name="simulation_lens",
        recommendation=recommendation,
        blockers=blockers,
        notes=notes
    )

def evaluate_governance_lens(context: Dict[str, Any]) -> CouncilVoteLikeRecord:
    blockers = []
    notes = []
    recommendation = CouncilDecisionType.APPROVE_HANDOFF

    if not context.get("approvals_complete", False):
        notes.append("Missing final approvals.")
        recommendation = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

    if not context.get("docs_linked", False):
        notes.append("Missing required documentation links.")
        recommendation = CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE

    return CouncilVoteLikeRecord(
        vote_id=str(uuid.uuid4()),
        lens_name="governance_lens",
        recommendation=recommendation,
        blockers=blockers,
        notes=notes
    )

def evaluate_rollout_history_lens(context: Dict[str, Any]) -> CouncilVoteLikeRecord:
    blockers = []
    notes = []
    recommendation = CouncilDecisionType.APPROVE_HANDOFF

    stability = context.get("stability_score", 1.0)
    if stability < 0.8:
        blockers.append("Unstable rollout history across stages.")
        recommendation = CouncilDecisionType.REJECT_HANDOFF

    return CouncilVoteLikeRecord(
        vote_id=str(uuid.uuid4()),
        lens_name="rollout_history_lens",
        recommendation=recommendation,
        blockers=blockers,
        notes=notes
    )

def aggregate_council_lenses(votes: List[CouncilVoteLikeRecord]) -> CouncilDecisionType:
    recs = [v.recommendation for v in votes]

    if any(r == CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF for r in recs):
        return CouncilDecisionType.KILL_CANDIDATE_BEFORE_HANDOFF

    if any(r == CouncilDecisionType.REJECT_HANDOFF for r in recs):
        return CouncilDecisionType.REJECT_HANDOFF

    holds = [r for r in recs if "HOLD" in r.value or "REQUIRE" in r.value]
    if holds:
        return CouncilDecisionType.MIXED_HOLD

    if all(r == CouncilDecisionType.APPROVE_HANDOFF for r in recs):
        return CouncilDecisionType.UNANIMOUS_APPROVE

    return CouncilDecisionType.APPROVE_WITH_CAVEATS
