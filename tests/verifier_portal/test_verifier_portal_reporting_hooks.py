from sports_signal_bot.verifier_portal.reporting import get_verifier_portal_reporting

def test_get_verifier_portal_reporting():
    reporting = get_verifier_portal_reporting()
    assert reporting["reporting"] == "ok"
