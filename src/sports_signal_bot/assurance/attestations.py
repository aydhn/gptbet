import uuid
from typing import List
from .contracts import AssuranceAttestationRecord, AttestationIssuerFamily, AttestationStatus

def build_assurance_attestation(
    issuer_family: AttestationIssuerFamily,
    target_ref: str,
    claim_refs: List[str],
    status: AttestationStatus = AttestationStatus.valid
) -> AssuranceAttestationRecord:
    return AssuranceAttestationRecord(
        attestation_id=f"att_{uuid.uuid4().hex[:8]}",
        attestation_family=issuer_family,
        issuer_ref=f"issuer_{issuer_family.value}_system",
        target_ref=target_ref,
        claim_refs=claim_refs,
        attestation_status=status,
        signature_or_proof_ref=f"sig_{uuid.uuid4().hex[:12]}"
    )
