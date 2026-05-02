import uuid
from typing import List, Dict, Any

from src.sports_signal_bot.capability_negotiation.contracts import (
    FederationPolicyRecord,
    FederationVerifierClassRecord,
    FederationAcceptanceRuleRecord,
    FederationReviewRequirementRecord,
    FederationDowngradeRuleRecord,
    CapabilityProfileRecord
)

def resolve_federation_policy(policy_data: Dict[str, Any]) -> FederationPolicyRecord:
    classes = [FederationVerifierClassRecord(**c) for c in policy_data.get("verifier_classes", [])]
    rules = [FederationAcceptanceRuleRecord(**r) for r in policy_data.get("acceptance_rules", [])]
    reviews = [FederationReviewRequirementRecord(**r) for r in policy_data.get("review_requirements", [])]
    downgrades = [FederationDowngradeRuleRecord(**r) for r in policy_data.get("downgrade_rules", [])]

    return FederationPolicyRecord(
        policy_id=policy_data.get("policy_id", str(uuid.uuid4())),
        verifier_classes=classes,
        acceptance_rules=rules,
        review_requirements=reviews,
        downgrade_rules=downgrades
    )

def evaluate_verifier_federation_policy(policy: FederationPolicyRecord, verifier_profile: CapabilityProfileRecord) -> bool:
    """
    Evaluates if a verifier profile meets the baseline federation policy.
    """
    if not policy.verifier_classes:
         return True # Open policy

    # In a real scenario, map profile attributes to classes.
    # Here, we do a basic check: must support at least one artifact family.
    if not verifier_profile.supported_artifact_families:
        return False

    return True
