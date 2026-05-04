from sports_signal_bot.capability_negotiation.profiles import build_capability_profile
from sports_signal_bot.capability_negotiation.federation_policies import resolve_federation_policy
from sports_signal_bot.capability_negotiation.onboarding import onboard_external_verifier_capabilities

def test_onboarding():
    policy = resolve_federation_policy({
        "verifier_classes": [{"class_id": "tier1", "description": ""}]
    })

    # Missing proof formats -> quarantine
    profile1 = build_capability_profile("v1", supported_artifact_families=["a"])
    rec1 = onboard_external_verifier_capabilities("v1", profile1, policy)
    assert rec1.status == "quarantined_pending_review"

    # Has proof formats -> accepted
    profile2 = build_capability_profile("v2", supported_artifact_families=["a"], supported_proof_formats=["jwt"])
    rec2 = onboard_external_verifier_capabilities("v2", profile2, policy)
    assert rec2.status == "accepted"
