from typing import List
from sports_signal_bot.federation_ecosystem.contracts import (
    SovereignPolicyAttestationEcosystemRecord, EcosystemParticipantRecord,
    IssuerCapabilityRecord, PolicyAttestationProfileRecord
)

def build_policy_attestation_ecosystem(ecosystem_id: str, family: str) -> SovereignPolicyAttestationEcosystemRecord:
    return SovereignPolicyAttestationEcosystemRecord(
        ecosystem_id=ecosystem_id,
        ecosystem_family=family,
        participant_refs=[],
        hub_refs=[],
        registry_refs=[],
        baseline_catalog_refs=[],
        supported_attestation_families=[],
        participation_policy_ref="default",
        health_status="healthy",
        warnings=[]
    )

def register_ecosystem_participant(ecosystem: SovereignPolicyAttestationEcosystemRecord, participant: EcosystemParticipantRecord) -> SovereignPolicyAttestationEcosystemRecord:
    ecosystem.participant_refs.append(participant.participant_id)
    return ecosystem

def evaluate_participation_state(participant: EcosystemParticipantRecord) -> str:
    if participant.participation_status in ["participating_suspended", "participating_expired", "participating_removed"]:
        return "inactive"
    return "active"

def summarize_ecosystem_health(ecosystem: SovereignPolicyAttestationEcosystemRecord) -> str:
    return ecosystem.health_status

def build_issuer_capability_profile(families: List[str], max_scope: str) -> IssuerCapabilityRecord:
    return IssuerCapabilityRecord(
        supported_attestation_families=families,
        max_scope_class=max_scope,
        caveat_handling_support=True,
        validity_window_support=True,
        exchange_scope_support=True,
        replay_evidence_support=True,
        degraded_exchange_support=False,
        sovereignty_override_support=False
    )

def validate_issuer_for_exchange_scope(capability: IssuerCapabilityRecord, requested_scope: str) -> bool:
    if capability.max_scope_class == "bounded" and requested_scope == "unbounded":
        return False
    return True

def prevent_issuer_scope_overclaim(capability: IssuerCapabilityRecord, claim: str) -> IssuerCapabilityRecord:
    if claim == "unbounded":
        capability.max_scope_class = "bounded"
    return capability

def summarize_issuer_capability(capability: IssuerCapabilityRecord) -> str:
    return f"Max Scope: {capability.max_scope_class}, Caveat Handling: {capability.caveat_handling_support}"

def build_policy_attestation_profile(visibility: str) -> PolicyAttestationProfileRecord:
    return PolicyAttestationProfileRecord(
        supported_dimensions=[],
        supported_caveat_classes=[],
        exchange_visibility=visibility,
        benchmark_attachment_support=True,
        conformance_pack_linkage_support=True,
        registry_projection_support=True
    )

def compare_profiles_for_interop(profile1: PolicyAttestationProfileRecord, profile2: PolicyAttestationProfileRecord) -> bool:
    return profile1.exchange_visibility == profile2.exchange_visibility

def summarize_profile_fit(profile: PolicyAttestationProfileRecord) -> str:
    return profile.exchange_visibility
