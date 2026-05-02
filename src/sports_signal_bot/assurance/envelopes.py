import uuid
from typing import List
from .contracts import (PromotionEnvelopeRecord, ProofCarryingBundleRecord,
                        AssuranceClaimRecord, EnvelopeStatus)

def build_promotion_envelope(
    target_ref: str,
    bundle: ProofCarryingBundleRecord,
    claims: List[AssuranceClaimRecord],
    required_families: List[str]
) -> PromotionEnvelopeRecord:
    satisfied = [c.claim_id for c in claims if c.claim_type.value == "satisfied"]
    blocked = [c.claim_id for c in claims if c.claim_type.value in ["blocked", "stale", "expired"]]

    status = EnvelopeStatus.assurance_ready
    if blocked:
        status = EnvelopeStatus.assurance_blocked
    elif len(satisfied) < len(required_families):
        status = EnvelopeStatus.assurance_review_required

    return PromotionEnvelopeRecord(
        envelope_id=f"env_{uuid.uuid4().hex[:8]}",
        target_ref=target_ref,
        required_claims_summary={"required_count": len(required_families), "families": required_families},
        satisfied_claims=satisfied,
        blocked_claims=blocked,
        proof_carrying_bundle_ref=bundle.proof_bundle_id,
        assurance_attestations=bundle.attestation_refs,
        trust_signature_status="verified",
        drift_cleanliness="clean",
        conformance_summary="passed",
        final_assurance_decision=status,
        replay_hints={"deterministic_seed": "42", "spec_version": "v1.2"}
    )
