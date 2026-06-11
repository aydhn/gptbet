from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from .contracts import DecisionProofRecord, DecisionProofParameters, SignerStatus, VerificationStatus
from .canonicalization import compute_decision_hash

def build_decision_proof(params: DecisionProofParameters) -> DecisionProofRecord:
    """Builds an immutable decision proof record."""
    input_hash = compute_decision_hash(params.inputs)
    output_hash = compute_decision_hash(params.outputs)

    proof_payload = {
        "decision_ref": params.decision_ref,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "applied_policy_snapshot_ref": params.applied_policy_snapshot_ref
    }
    proof_hash = compute_decision_hash(proof_payload)

    return DecisionProofRecord(
        decision_proof_id=f"proof_{uuid.uuid4().hex[:8]}",
        decision_family=params.decision_family,
        decision_ref=params.decision_ref,
        applied_policy_snapshot_ref=params.applied_policy_snapshot_ref,
        evidence_refs=params.evidence_refs,
        input_hash=input_hash,
        output_hash=output_hash,
        proof_hash=proof_hash,
        prior_proof_ref=params.prior_proof_ref,
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
