from typing import Dict, Any

from .contracts import DecisionProofRecord

def build_evidence_from_proof(proof: DecisionProofRecord) -> Dict[str, Any]:
    """Extracts a structured evidence view from a decision proof."""
    return {
        "proof_id": proof.decision_proof_id,
        "decision_family": proof.decision_family,
        "input_hash": proof.input_hash,
        "output_hash": proof.output_hash,
        "verification_status": proof.verification_status.value,
        "is_valid": proof.verification_status == "valid",
        "created_at": proof.created_at.isoformat()
    }
