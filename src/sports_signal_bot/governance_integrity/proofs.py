from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from .contracts import DecisionProofRecord, SignerStatus, VerificationStatus
from .canonicalization import compute_decision_hash

def build_decision_proof(
    decision_family: str,
    decision_ref: str,
    applied_policy_snapshot_ref: str,
    inputs: Dict[str, Any],
    outputs: Dict[str, Any],
    evidence_refs: List[str] = None,
    prior_proof_ref: Optional[str] = None
) -> DecisionProofRecord:
    """Builds an immutable decision proof record."""
    input_hash = compute_decision_hash(inputs)
    output_hash = compute_decision_hash(outputs)

    proof_payload = {
        "decision_ref": decision_ref,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "applied_policy_snapshot_ref": applied_policy_snapshot_ref
    }
    proof_hash = compute_decision_hash(proof_payload)

    return DecisionProofRecord(
        decision_proof_id=f"proof_{uuid.uuid4().hex[:8]}",
        decision_family=decision_family,
        decision_ref=decision_ref,
        applied_policy_snapshot_ref=applied_policy_snapshot_ref,
        evidence_refs=evidence_refs or [],
        input_hash=input_hash,
        output_hash=output_hash,
        proof_hash=proof_hash,
        prior_proof_ref=prior_proof_ref,
        signer_status=SignerStatus.ACTIVE,
        verification_status=VerificationStatus.VALID,
        created_at=datetime.utcnow()
    )

def link_proof_chain(proofs: List[DecisionProofRecord]) -> bool:
    """Validates that a list of proofs forms an unbroken chain."""
    for i in range(1, len(proofs)):
        if proofs[i].prior_proof_ref != proofs[i-1].decision_proof_id:
            return False
    return True
