from typing import Dict, List, Optional
from .contracts import PublicationProfileRecord, VerifierProfileRecord, ExternalVerifierOnrampRecord, VerifierAccessPolicyRecord

class PublicationProfileManager:
    def __init__(self, profiles: Optional[List[PublicationProfileRecord]] = None):
        self.profiles = {p.profile_id: p for p in (profiles or [])}

    def register_profile(self, profile: PublicationProfileRecord) -> None:
        self.profiles[profile.profile_id] = profile

    def get_profile(self, profile_id: str) -> Optional[PublicationProfileRecord]:
        return self.profiles.get(profile_id)

    def list_profiles(self) -> List[PublicationProfileRecord]:
        return list(self.profiles.values())

def get_default_profiles() -> List[PublicationProfileRecord]:
    return [
        PublicationProfileRecord(
            profile_id="public_minimal",
            profile_name="Public Minimal",
            audience_family="public",
            redaction_level="strict",
            allowed_item_families=["policy_bundle_disclosure", "transparency_checkpoint_disclosure", "readiness_summary_disclosure"],
            forbidden_field_families=["signer_metadata", "internal_paths", "operator_notes", "secret", "trust_private"],
            proof_depth="shallow",
            notarization_visibility="summary",
            challenge_intake_allowed=False
        ),
        PublicationProfileRecord(
            profile_id="public_verifier",
            profile_name="Public Verifier",
            audience_family="public",
            redaction_level="moderate",
            allowed_item_families=["policy_bundle_disclosure", "transparency_checkpoint_disclosure", "decision_proof_disclosure", "notarization_summary_disclosure", "readiness_summary_disclosure"],
            forbidden_field_families=["internal_paths", "operator_notes", "secret", "trust_private"],
            proof_depth="moderate",
            notarization_visibility="detailed",
            challenge_intake_allowed=True
        ),
        PublicationProfileRecord(
            profile_id="external_auditor",
            profile_name="External Auditor",
            audience_family="auditor",
            redaction_level="relaxed",
            allowed_item_families=[
                "policy_bundle_disclosure", "transparency_checkpoint_disclosure", "decision_proof_disclosure",
                "witness_consensus_disclosure", "anomaly_summary_disclosure", "notarization_summary_disclosure",
                "external_exchange_summary_disclosure", "readiness_summary_disclosure", "governance_health_summary_disclosure"
            ],
            forbidden_field_families=["operator_notes", "secret"],
            proof_depth="deep",
            notarization_visibility="full",
            challenge_intake_allowed=True
        ),
        PublicationProfileRecord(
            profile_id="trusted_exchange_partner",
            profile_name="Trusted Exchange Partner",
            audience_family="partner",
            redaction_level="relaxed",
            allowed_item_families=["policy_bundle_disclosure", "transparency_checkpoint_disclosure", "decision_proof_disclosure", "external_exchange_summary_disclosure", "witness_consensus_disclosure"],
            forbidden_field_families=["secret", "operator_notes"],
            proof_depth="deep",
            notarization_visibility="full",
            challenge_intake_allowed=True
        ),
        PublicationProfileRecord(
            profile_id="review_quarantine_external",
            profile_name="Review Quarantine External",
            audience_family="reviewer",
            redaction_level="moderate",
            allowed_item_families=["policy_bundle_disclosure", "transparency_checkpoint_disclosure", "anomaly_summary_disclosure", "notarization_summary_disclosure"],
            forbidden_field_families=["internal_paths", "operator_notes", "secret", "trust_private"],
            proof_depth="shallow",
            notarization_visibility="summary",
            challenge_intake_allowed=False
        ),
        PublicationProfileRecord(
            profile_id="internal_publication_preview",
            profile_name="Internal Publication Preview",
            audience_family="internal",
            redaction_level="none",
            allowed_item_families=[
                "policy_bundle_disclosure", "transparency_checkpoint_disclosure", "decision_proof_disclosure",
                "witness_consensus_disclosure", "anomaly_summary_disclosure", "notarization_summary_disclosure",
                "external_exchange_summary_disclosure", "readiness_summary_disclosure", "governance_health_summary_disclosure"
            ],
            forbidden_field_families=[],
            proof_depth="full",
            notarization_visibility="full",
            challenge_intake_allowed=False
        )
    ]

class ExternalVerifierOnramp:
    def __init__(self):
        self.verifiers: Dict[str, VerifierProfileRecord] = {}
        self.onramps: Dict[str, ExternalVerifierOnrampRecord] = {}
        self.policies: Dict[str, VerifierAccessPolicyRecord] = {}

    def register_external_verifier_profile(self, profile: VerifierProfileRecord) -> None:
        self.verifiers[profile.profile_id] = profile

    def assign_publication_profile_to_verifier(self, policy: VerifierAccessPolicyRecord) -> None:
        self.policies[policy.policy_id] = policy

    def validate_verifier_onramp(self, onramp_id: str) -> bool:
        return onramp_id in self.onramps

    def summarize_verifier_access(self, verifier_id: str) -> Dict:
        allowed_profiles = []
        for policy in self.policies.values():
            # In a real implementation we'd link policy to verifier
            if policy.profile_id in [v.profile_id for v in self.verifiers.values()]:
                allowed_profiles.extend(policy.allowed_publication_profiles)

        return {
            "verifier_id": verifier_id,
            "allowed_publication_profiles": list(set(allowed_profiles)),
            "status": "active"
        }
