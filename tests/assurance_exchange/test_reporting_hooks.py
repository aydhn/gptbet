from sports_signal_bot.assurance_exchange.reporting import build_assurance_exchange_summary

def test_build_assurance_exchange_summary():
    res = build_assurance_exchange_summary([], [], [], [], [], [])
    assert res["federated_registry_count"] == 0
