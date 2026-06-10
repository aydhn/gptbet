from sports_signal_bot.capability_negotiation.federation_policies import (
    resolve_federation_policy,
    evaluate_verifier_federation_policy,
)
from sports_signal_bot.capability_negotiation.profiles import (
    build_capability_profile
)


def test_evaluate_verifier_federation_policy_open_policy():
    policy = resolve_federation_policy({
        "verifier_classes": []
    })

    # Empty supported_artifact_families
    profile1 = build_capability_profile("v1")
    assert evaluate_verifier_federation_policy(policy, profile1) is True

    # With supported_artifact_families
    profile2 = build_capability_profile(
        "v2", supported_artifact_families=["a"]
    )
    assert evaluate_verifier_federation_policy(policy, profile2) is True


def test_evaluate_verifier_federation_policy_with_classes_valid_profile():
    policy = resolve_federation_policy({
        "verifier_classes": [
            {"class_id": "tier1", "description": "Tier 1 Verifier"}
        ]
    })

    # With supported_artifact_families
    profile = build_capability_profile(
        "v1", supported_artifact_families=["a"]
    )
    assert evaluate_verifier_federation_policy(policy, profile) is True


def test_evaluate_verifier_federation_policy_with_classes_invalid_profile():
    policy = resolve_federation_policy({
        "verifier_classes": [
            {"class_id": "tier1", "description": "Tier 1 Verifier"}
        ]
    })

    # Empty supported_artifact_families
    profile = build_capability_profile("v1")
    assert evaluate_verifier_federation_policy(policy, profile) is False
