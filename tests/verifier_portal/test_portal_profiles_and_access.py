from sports_signal_bot.verifier_portal.profiles import get_profile
from sports_signal_bot.verifier_portal.access import evaluate_portal_access

def test_get_profile():
    profile = get_profile("public_viewer")
    assert profile.profile_id == "public_viewer"
    assert not profile.challenge_submission_rights

    profile = get_profile("external_auditor")
    assert profile.profile_id == "external_auditor"
    assert profile.challenge_submission_rights

def test_evaluate_portal_access():
    decision = evaluate_portal_access("public_viewer", "view", "publication_index_view")
    assert decision.decision == "allowed"

    decision = evaluate_portal_access("public_viewer", "challenge_submission", "submit")
    assert decision.decision == "denied"

    decision = evaluate_portal_access("registered_verifier", "challenge_submission", "submit")
    assert decision.decision == "allowed"
