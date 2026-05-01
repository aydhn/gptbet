from datetime import datetime
from typing import List, Optional
from .contracts import (
    AttestationStatementRecord,
    AttestationProviderRecord,
    AttestationVerificationRecord,
    AttestationStatus,
    AttestationTrustEffectRecord,
    AttestationRecord
)

def collect_external_attestations(
    target_ref: str
) -> List[AttestationStatementRecord]:
    # Placeholder for fetching external attestations
    return []

def verify_attestation_statement(
    statement: AttestationStatementRecord,
    provider: Optional[AttestationProviderRecord]
) -> AttestationVerificationRecord:
    if not provider:
        status = AttestationStatus.PROVIDER_UNTRUSTED
    elif statement.expires_at and datetime.utcnow() > statement.expires_at:
        status = AttestationStatus.STALE
    else:
        # Simplified verification
        status = AttestationStatus.VALID_SUPPORTING

    trust_effect = None
    if status == AttestationStatus.VALID_SUPPORTING and provider:
        trust_effect = AttestationTrustEffectRecord(
            applied_boost=provider.trust_weight_boost_cap,
            conditions=["provider_trusted", "not_expired"]
        )

    return AttestationVerificationRecord(
        verification_id=f"ver_{datetime.utcnow().timestamp()}",
        statement_ref=statement.statement_id,
        status=status,
        trust_effect=trust_effect,
        verified_at=datetime.utcnow()
    )

def bound_attestation_influence(
    base_trust: float,
    attestation_boost: float,
    max_boost_cap: float = 0.5
) -> float:
    # Ensures attestation does not override local trust
    bounded_boost = min(attestation_boost, max_boost_cap)
    # E.g. never let attestation account for more than 30% of total trust
    if bounded_boost > (base_trust * 0.3):
        bounded_boost = base_trust * 0.3

    return round(bounded_boost, 2)

def integrate_attestation_with_threshold(
    base_trust: float,
    verifications: List[AttestationVerificationRecord]
) -> float:
    total_boost = 0.0
    for v in verifications:
        if v.status == AttestationStatus.VALID_SUPPORTING and v.trust_effect:
            total_boost += v.trust_effect.applied_boost

    # Apply bounding
    bounded_boost = bound_attestation_influence(base_trust, total_boost)
    return round(base_trust + bounded_boost, 2)
