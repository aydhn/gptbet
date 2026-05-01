from typing import Dict, Any, List, Optional
import uuid
from .contracts import (
    EscalationCaseRecord, EscalationOutcome, EscalationOutcomeRecord,
    ControlPlaneRecord
)

def detect_escalation_need(condition_met: bool, severity: str) -> bool:
    if condition_met and severity in ["high", "critical"]:
        return True
    return False

def build_escalation_case(source_plane_id: str, target_plane_id: str, reason: str, context: Dict[str, Any] = None) -> EscalationCaseRecord:
    return EscalationCaseRecord(
        case_id=f"esc_{uuid.uuid4().hex[:8]}",
        source_plane_id=source_plane_id,
        target_plane_id=target_plane_id,
        reason=reason,
        context=context or {}
    )

def route_escalation(case: EscalationCaseRecord, target_plane: ControlPlaneRecord) -> EscalationCaseRecord:
    case.target_plane_id = target_plane.plane_id
    case.status = "routed"
    return case

def resolve_escalation_outcome(case_id: str, outcome: EscalationOutcome, rationale: str) -> EscalationOutcomeRecord:
    return EscalationOutcomeRecord(
        outcome_id=f"out_{uuid.uuid4().hex[:8]}",
        case_id=case_id,
        outcome=outcome,
        rationale=rationale
    )

def summarize_escalation_path(case: EscalationCaseRecord, outcome: Optional[EscalationOutcomeRecord] = None) -> str:
    res = f"Escalation {case.case_id}: {case.source_plane_id} -> {case.target_plane_id} ({case.reason})"
    if outcome:
        res += f" => {outcome.outcome.value}"
    return res
