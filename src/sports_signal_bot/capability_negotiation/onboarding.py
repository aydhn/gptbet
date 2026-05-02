import uuid
from typing import Dict, Any

from src.sports_signal_bot.capability_negotiation.contracts import (
    VerifierOnboardingRecord,
    CapabilityProfileRecord
)
from src.sports_signal_bot.capability_negotiation.federation_policies import (
    FederationPolicyRecord,
    evaluate_verifier_federation_policy
)

def onboard_external_verifier_capabilities(
    verifier_ref: str,
    profile: CapabilityProfileRecord,
    policy: FederationPolicyRecord
) -> VerifierOnboardingRecord:

    is_valid = evaluate_verifier_federation_policy(policy, profile)

    status = "accepted" if is_valid else "quarantined_pending_review"

    # Check for unsupported proof formats as a quarantine trigger
    if not profile.supported_proof_formats:
        status = "quarantined_pending_review"

    return VerifierOnboardingRecord(
        onboarding_id=str(uuid.uuid4()),
        verifier_ref=verifier_ref,
        profile=profile,
        status=status
    )
