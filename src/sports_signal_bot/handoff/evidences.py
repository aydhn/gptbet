import uuid
from typing import Dict, Any, List
from .contracts import HandoffEvidenceMatrixRecord

def build_handoff_evidence_packet(handoff_id: str, context: Dict[str, Any], decision_ref: str) -> HandoffEvidenceMatrixRecord:
    explanations = {}
    citations = []

    # Evidence mapping logic based on phase 40 integration requirements
    if context.get("evidence_score", 0.0) >= 0.8:
        explanations["strong_evidence"] = "Candidate is backed by strong simulation and backtesting evidence."
        citations.append(f"sim_run_{uuid.uuid4().hex[:8]}")
    else:
        explanations["weak_evidence"] = "Candidate lacks sufficient historical evidence."

    if context.get("approvals_complete", False):
         explanations["governance"] = "All required sign-offs have been captured."
         citations.append("approval_ledger_id_xxx")

    return HandoffEvidenceMatrixRecord(
        evidence_matrix_id=str(uuid.uuid4()),
        handoff_id=handoff_id,
        citations=citations,
        explanations=explanations
    )

def explain_council_decision(decision_ref: str, context: Dict[str, Any]) -> str:
    # A formatted text explanation
    return f"Decision rationale: Context score was {context.get('readiness_score', 0)}."
