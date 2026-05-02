import uuid
from typing import List
from .contracts import ProofCarryingBundleRecord, AssuranceClaimRecord

def build_proof_carrying_bundle(
    target_ref: str,
    claims: List[AssuranceClaimRecord],
    attestation_refs: List[str]
) -> ProofCarryingBundleRecord:
    claim_refs = [c.claim_id for c in claims]
    ev_refs = [ev for c in claims for ev in c.evidence_refs]
    prf_refs = [prf for c in claims for prf in c.proof_refs]

    return ProofCarryingBundleRecord(
        proof_bundle_id=f"pcb_{uuid.uuid4().hex[:8]}",
        bundle_family="promotion_candidate_assurance_bundle",
        target_ref=target_ref,
        carried_claim_refs=claim_refs,
        evidence_refs=list(set(ev_refs)),
        proof_refs=list(set(prf_refs)),
        attestation_refs=attestation_refs,
        spec_refs=["spec_v1_0"]
    )
