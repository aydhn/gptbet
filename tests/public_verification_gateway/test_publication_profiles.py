from src.sports_signal_bot.public_verification_gateway.profiles import get_default_profiles, PublicationProfileManager

def test_default_profiles():
    profiles = get_default_profiles()
    assert len(profiles) > 0
    manager = PublicationProfileManager(profiles)

    pm = manager.get_profile("public_minimal")
    assert pm is not None
    assert not pm.challenge_intake_allowed
    assert "public" == pm.audience_family

    pv = manager.get_profile("public_verifier")
    assert pv is not None
    assert pv.challenge_intake_allowed
