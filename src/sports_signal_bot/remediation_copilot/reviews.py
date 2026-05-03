import uuid
from typing import List
from .contracts import CopilotReviewPacketRecord

def build_copilot_review_packet(
    session_id: str,
    incident_summary: str,
    matched_patterns: List[str],
    confidence_score: float,
    selected_playbook_rationale: str,
    scoped_steps: List[str],
    required_guards: List[str],
    rehearsal_proposal: str,
    rollback_notes: str,
    expected_signals: List[str],
    stop_conditions: List[str],
    approval_requirements: List[str]
) -> CopilotReviewPacketRecord:
    return CopilotReviewPacketRecord(
        packet_id=f"rev_{uuid.uuid4().hex[:8]}",
        session_id=session_id,
        incident_summary=incident_summary,
        matched_patterns=matched_patterns,
        confidence_score=confidence_score,
        selected_playbook_rationale=selected_playbook_rationale,
        scoped_steps=scoped_steps,
        rejected_step_alternatives=[],
        required_guards=required_guards,
        rehearsal_proposal=rehearsal_proposal,
        rollback_notes=rollback_notes,
        expected_signals=expected_signals,
        stop_conditions=stop_conditions,
        approval_requirements=approval_requirements,
        caveats=[]
    )
