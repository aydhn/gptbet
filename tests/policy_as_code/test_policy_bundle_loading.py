import pytest
from sports_signal_bot.policy_as_code.contracts import PolicyBundleRecord, PolicyReviewStatus

def test_policy_bundle_loading():
    bundle = PolicyBundleRecord(
        policy_bundle_id="b1",
        bundle_name="Test Bundle",
        bundle_family="test",
        version="v1",
        status=PolicyReviewStatus.ACTIVE,
        rules=["r1", "r2"]
    )
    assert bundle.policy_bundle_id == "b1"
    assert bundle.bundle_name == "Test Bundle"
    assert bundle.bundle_family == "test"
    assert bundle.version == "v1"
    assert bundle.status == PolicyReviewStatus.ACTIVE
    assert bundle.rules == ["r1", "r2"]
