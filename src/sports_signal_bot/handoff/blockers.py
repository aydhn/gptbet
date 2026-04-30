import uuid
from typing import List, Dict, Any
from .contracts import HandoffBlockerRecord, HandoffKillReason

def collect_council_blockers(handoff_id: str, candidate_state: Dict[str, Any]) -> List[HandoffBlockerRecord]:
    blockers = []

    if candidate_state.get("evidence_completeness", 0) < 0.8:
        blockers.append(HandoffBlockerRecord(
            blocker_id=str(uuid.uuid4()),
            handoff_id=handoff_id,
            severity="high",
            description="Evidence completeness is below the required 80% threshold."
        ))

    if candidate_state.get("unresolved_disputes", 0) > 0:
        blockers.append(HandoffBlockerRecord(
            blocker_id=str(uuid.uuid4()),
            handoff_id=handoff_id,
            severity="critical",
            description=f"Candidate has {candidate_state['unresolved_disputes']} unresolved disputes."
        ))

    if candidate_state.get("gate_freshness_hours", 0) > 24:
         blockers.append(HandoffBlockerRecord(
            blocker_id=str(uuid.uuid4()),
            handoff_id=handoff_id,
            severity="medium",
            description="Quality gates are older than 24 hours. Fresh runs required."
        ))

    return blockers

def detect_kill_before_handoff_conditions(handoff_id: str, candidate_state: Dict[str, Any]) -> HandoffKillReason:
    if candidate_state.get("is_stale", False):
        return HandoffKillReason.STALE_CANDIDATE_PACKAGE

    if candidate_state.get("critical_blocker_count", 0) > 0:
        return HandoffKillReason.UNRESOLVED_CRITICAL_BLOCKERS

    if candidate_state.get("is_superseded", False):
        return HandoffKillReason.SUPERSEDED_BY_NARROWER_SAFER_CANDIDATE

    if candidate_state.get("failed_fresh_gates", False):
        return HandoffKillReason.FAILED_FRESH_GATE_REQUIREMENTS

    if candidate_state.get("rollback_notes_complete") is False:
        return HandoffKillReason.INCOMPLETE_ROLLBACK_NOTES

    if candidate_state.get("approval_window_expired", False):
        return HandoffKillReason.MISSING_FINAL_APPROVAL_WITH_EXPIRED_WINDOW

    return HandoffKillReason.NOT_KILLED

def classify_kill_before_handoff_reason(reason: HandoffKillReason) -> str:
    if reason == HandoffKillReason.NOT_KILLED:
        return "Eligible for handoff"
    return f"Candidate killed: {reason.value.replace('_', ' ').capitalize()}"
