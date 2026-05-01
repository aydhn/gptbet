from sports_signal_bot.multi_signer_trust.reporting import quorum_success_rate

def test_reporting_hooks():
    assert quorum_success_rate() >= 0.0
