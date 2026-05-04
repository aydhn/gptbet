from sports_signal_bot.capability_negotiation.registry_notarization import request_registry_notarization, verify_registry_notarization

def test_registry_notarization():
    data = {"state": "active"}
    notarization = request_registry_notarization("reg1", data)

    assert verify_registry_notarization(notarization, data) is True
    assert verify_registry_notarization(notarization, {"state": "inactive"}) is False
