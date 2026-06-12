import uuid
from typing import List
from .contracts import CopilotReviewPacketRecord, CopilotReviewPacketParams

def build_copilot_review_packet(
    params: CopilotReviewPacketParams
) -> CopilotReviewPacketRecord:
    return CopilotReviewPacketRecord(
        packet_id=f"rev_{uuid.uuid4().hex[:8]}",
        session_id=params.session_id,
        incident_summary=params.incident_summary,
        matched_patterns=params.matched_patterns,
        confidence_score=params.confidence_score,
        selected_playbook_rationale=params.selected_playbook_rationale,
        scoped_steps=params.scoped_steps,
        rejected_step_alternatives=[],
        required_guards=params.required_guards,
        rehearsal_proposal=params.rehearsal_proposal,
        rollback_notes=params.rollback_notes,
        expected_signals=params.expected_signals,
        stop_conditions=params.stop_conditions,
        approval_requirements=params.approval_requirements,
        caveats=[]
    )
