from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import (
    RegionalAssuranceContinuityControllerRecord,
    ContinuityDecisionRecord,
    ContinuityGapRecord
)

def start_continuity_controller_session(controller_id: str) -> RegionalAssuranceContinuityControllerRecord:
    return RegionalAssuranceContinuityControllerRecord(
        controller_id=controller_id,
        controller_family="default",
        continuity_policy_ref="default",
        decision_status="monitoring"
    )

def collect_continuity_signals(controller: RegionalAssuranceContinuityControllerRecord) -> List[str]:
    return ["checkpoint_1", "checkpoint_2"]

def escalate_continuity_gap(controller: RegionalAssuranceContinuityControllerRecord, gap: ContinuityGapRecord) -> RegionalAssuranceContinuityControllerRecord:
    if gap.severity in ["high", "critical"]:
        controller.decision_status = "blocked"
        controller.warnings.append(f"escalated gap: {gap.gap_id}")
    return controller

def finalize_continuity_controller_decision(controller: RegionalAssuranceContinuityControllerRecord) -> ContinuityDecisionRecord:
    if controller.decision_status == "blocked":
        outcome = "continuity_blocked"
    elif controller.warnings:
        outcome = "continuity_verified_with_caveats"
    else:
        outcome = "continuity_verified"

    return ContinuityDecisionRecord(
        decision_id=f"dec_{controller.controller_id}",
        outcome=outcome
    )

def summarize_controller_session(controller: RegionalAssuranceContinuityControllerRecord) -> Dict[str, Any]:
    return {
        "controller_id": controller.controller_id,
        "status": controller.decision_status,
        "warnings": len(controller.warnings)
    }

def classify_continuity_decision(outcome: str) -> str:
    return outcome

def map_gaps_to_continuity_outcome(gaps: List[ContinuityGapRecord]) -> str:
    severities = [g.severity for g in gaps]
    if "critical" in severities:
        return "continuity_blocked"
    if "high" in severities:
        return "continuity_review_required"
    if gaps:
        return "continuity_verified_with_caveats"
    return "continuity_verified"

def explain_continuity_blockers(gaps: List[ContinuityGapRecord]) -> List[str]:
    return [f"Blocked by {g.gap_id}" for g in gaps if g.severity in ["high", "critical"]]

def build_continuity_decision_packet(decision: ContinuityDecisionRecord) -> Dict[str, Any]:
    return {
        "decision": decision.outcome,
        "timestamp": "now"
    }
