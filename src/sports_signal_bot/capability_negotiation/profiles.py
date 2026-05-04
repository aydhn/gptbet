from typing import List, Dict, Any
import uuid

from sports_signal_bot.capability_negotiation.contracts import (
    CapabilityProfileRecord,
    CapabilityTrustConstraintRecord,
    CapabilityOfferRecord,
    CapabilityResponseRecord
)

def build_capability_profile(
    registry_or_verifier_ref: str,
    supported_artifact_families: List[str] = None,
    supported_claim_families: List[str] = None,
    supported_spec_families: List[str] = None,
    supported_versions: List[str] = None,
    supported_proof_formats: List[str] = None,
    supported_replay_modes: List[str] = None,
    supported_notarization_types: List[str] = None,
    supported_translation_modes: List[str] = None,
    supported_redaction_profiles: List[str] = None,
    trust_constraints: List[Dict[str, str]] = None,
    warnings: List[str] = None
) -> CapabilityProfileRecord:
    return CapabilityProfileRecord(
        profile_id=str(uuid.uuid4()),
        registry_or_verifier_ref=registry_or_verifier_ref,
        supported_artifact_families=supported_artifact_families or [],
        supported_claim_families=supported_claim_families or [],
        supported_spec_families=supported_spec_families or [],
        supported_versions=supported_versions or [],
        supported_proof_formats=supported_proof_formats or [],
        supported_replay_modes=supported_replay_modes or [],
        supported_notarization_types=supported_notarization_types or [],
        supported_translation_modes=supported_translation_modes or [],
        supported_redaction_profiles=supported_redaction_profiles or [],
        trust_constraints=[CapabilityTrustConstraintRecord(**tc) for tc in (trust_constraints or [])],
        warnings=warnings or []
    )

def build_capability_offer(profile: CapabilityProfileRecord, target_registry_ref: str) -> CapabilityOfferRecord:
    return CapabilityOfferRecord(
        offer_id=str(uuid.uuid4()),
        profile=profile,
        target_registry_ref=target_registry_ref
    )

def build_capability_response(offer_ref: str, profile: CapabilityProfileRecord) -> CapabilityResponseRecord:
    return CapabilityResponseRecord(
        response_id=str(uuid.uuid4()),
        offer_ref=offer_ref,
        profile=profile
    )
