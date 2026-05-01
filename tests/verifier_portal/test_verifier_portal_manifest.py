from sports_signal_bot.verifier_portal.manifests import get_verifier_portal_manifests

def test_get_verifier_portal_manifests():
    manifests = get_verifier_portal_manifests()
    assert manifests["manifest"] == "ok"
