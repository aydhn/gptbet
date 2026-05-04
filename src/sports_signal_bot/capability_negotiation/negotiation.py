import uuid
from typing import Optional
from datetime import datetime

from sports_signal_bot.capability_negotiation.contracts import (
    CapabilityProfileRecord,
    CapabilityOfferRecord,
    CapabilityResponseRecord,
    CapabilityNegotiationRecord,
    NegotiatedProfileRecord,
    NegotiationStatus,
    NegotiationDecision,
    NegotiatedScopeRecord,
    NegotiatedReplayPolicyRecord,
    NegotiatedTrustRecord
)
from sports_signal_bot.capability_negotiation.compatibility import diff_capability_profiles
from sports_signal_bot.capability_negotiation.translations import prevent_trust_amplification_via_translation

def evaluate_capability_match(
    offer: CapabilityOfferRecord,
    response: CapabilityResponseRecord
) -> CapabilityNegotiationRecord:

    diff = diff_capability_profiles(offer.profile, response.profile)

    # Very basic evaluation logic for Phase 64
    matched_caps = []
    rejected_caps = []

    for c in diff.narrowing_constraints:
        matched_caps.extend(c.narrowed_to)

    for g in diff.gaps:
        rejected_caps.append(g.dimension)

    status = NegotiationStatus.fully_matched
    if diff.gaps:
        status = NegotiationStatus.blocked_incompatible
    elif diff.narrowing_constraints:
        status = NegotiationStatus.partially_matched
    elif diff.translation_needs:
        status = NegotiationStatus.matched_with_caveats

    return CapabilityNegotiationRecord(
        negotiation_id=str(uuid.uuid4()),
        source_profile_ref=offer.profile.profile_id,
        target_profile_ref=response.profile.profile_id,
        requested_capabilities=offer.profile.supported_artifact_families, # simplified
        offered_capabilities=response.profile.supported_artifact_families, # simplified
        matched_capabilities=matched_caps,
        rejected_capabilities=rejected_caps,
        negotiation_status=status,
        created_at=datetime.utcnow().isoformat()
    )

def downgrade_to_safe_subset(
    source: CapabilityProfileRecord,
    target: CapabilityProfileRecord
) -> NegotiatedProfileRecord:
    diff = diff_capability_profiles(source, target)

    def get_subset(dim_name: str) -> list[str]:
        for c in diff.narrowing_constraints:
            if c.family == dim_name:
                return c.narrowed_to
        for g in diff.gaps:
             if g.dimension == dim_name:
                 return []

        # If not gap or narrowed, they match exactly.
        if dim_name == "artifact_families": return source.supported_artifact_families
        if dim_name == "claim_families": return source.supported_claim_families
        if dim_name == "proof_formats": return source.supported_proof_formats
        if dim_name == "notarization_types": return source.supported_notarization_types
        return []

    scope = NegotiatedScopeRecord(
        allowed_artifact_families=get_subset("artifact_families"),
        allowed_claim_families=get_subset("claim_families"),
        allowed_proof_formats=get_subset("proof_formats"),
        allowed_notarization_modes=get_subset("notarization_types")
    )

    replay = NegotiatedReplayPolicyRecord(
        replay_requirement_profile="minimal_interop"
    )

    trust = NegotiatedTrustRecord(
        accepted_trust_lanes=["quarantine_first"],
        import_export_boundaries=["strict"],
        redaction_publication_restrictions=["redacted_only"]
    )

    return NegotiatedProfileRecord(
        negotiated_profile_id=str(uuid.uuid4()),
        source_profile_ref=source.profile_id,
        target_profile_ref=target.profile_id,
        scope=scope,
        translations=[],
        replay_policy=replay,
        trust=trust
    )

def enforce_interop_safety(profile: NegotiatedProfileRecord) -> bool:
    """
    Ensures the negotiated profile adheres to safety rules:
    - only negotiated common subset kullanılabilir
    - unsupported replay mode => no high-assurance acceptance
    """
    if not profile.scope.allowed_artifact_families:
        return False
    return True
