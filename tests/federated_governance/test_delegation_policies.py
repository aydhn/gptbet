from sports_signal_bot.federated_governance.delegation import record_delegated_action, detect_overactive_plane, throttle_plane_delegation
from sports_signal_bot.federated_governance.contracts import DelegatedActionRecord

def test_record_delegated_action():
    action = record_delegated_action("plane1", "del1", {"foo": "bar"})
    assert action.plane_id == "plane1"
    assert action.status == "proposed"

def test_detect_overactive_plane():
    actions = [record_delegated_action("plane1", "del1", {}) for _ in range(11)]
    actions.append(record_delegated_action("plane2", "del2", {}))

    overactive = detect_overactive_plane(actions, threshold=10)
    assert "plane1" in overactive
    assert "plane2" not in overactive

def test_throttle_plane_delegation():
    throttle = throttle_plane_delegation("plane1", "Too many actions")
    assert throttle.plane_id == "plane1"
    assert throttle.active is True
