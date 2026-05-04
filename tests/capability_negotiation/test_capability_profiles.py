from sports_signal_bot.capability_negotiation.profiles import build_capability_profile

def test_build_capability_profile():
    profile = build_capability_profile(
        registry_or_verifier_ref="test_registry",
        supported_artifact_families=["assurance_bundle"]
    )
    assert profile.registry_or_verifier_ref == "test_registry"
    assert profile.supported_artifact_families == ["assurance_bundle"]
    assert profile.profile_id is not None
