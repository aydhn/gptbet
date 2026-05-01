from typing import Dict, Any, List
from .contracts import TrustPolicyRecord, TrustLevel, SignerRecord, SignerStatus

class TrustPolicyEvaluator:
    def __init__(self, policy: TrustPolicyRecord):
        self.policy = policy

    def resolve_trust_policy(self, environment: str) -> TrustLevel:
        """Returns the minimum trust level required for the environment."""
        return self.policy.minimum_trust_by_environment.get(environment, TrustLevel.ACTIVE)

    def validate_signer_scope(self, signer: SignerRecord, bundle_family: str) -> bool:
        """Checks if the signer is allowed to sign the bundle family."""
        if "*" in signer.signing_scope:
            return True
        if bundle_family in signer.signing_scope:
            return True

        allowed_signers = self.policy.allowed_signers_by_family.get(bundle_family, [])
        return signer.signer_id in allowed_signers

    def classify_signer_trust(self, signer: SignerRecord, environment: str) -> bool:
        """Checks if the signer meets the trust requirements for the environment."""
        if signer.active_status in (SignerStatus.REVOKED, SignerStatus.EXPIRED):
            return False

        required_trust = self.resolve_trust_policy(environment)

        # Simple trust hierarchy: DEV < REVIEW < ACTIVE < EMERGENCY
        trust_hierarchy = {
            TrustLevel.DEV: 1,
            TrustLevel.REVIEW: 2,
            TrustLevel.ACTIVE: 3,
            TrustLevel.EMERGENCY: 4,
            TrustLevel.REVOKED: 0
        }

        signer_score = trust_hierarchy.get(signer.trust_level, 0)
        required_score = trust_hierarchy.get(required_trust, 3)

        return signer_score >= required_score

    def is_unsigned_allowed(self) -> bool:
        return self.policy.allow_unsigned_dev

def get_default_trust_policy() -> TrustPolicyRecord:
    return TrustPolicyRecord(
        policy_id="default_policy_v1",
        allowed_signers_by_family={
            "critical_rules": ["admin_signer", "emergency_signer"],
            "growth_rules": ["review_signer", "admin_signer"]
        },
        minimum_trust_by_environment={
            "dev": TrustLevel.DEV,
            "staging": TrustLevel.REVIEW,
            "production": TrustLevel.ACTIVE
        },
        require_multi_review=True,
        allow_unsigned_dev=True
    )
