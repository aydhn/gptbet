import pytest
from sports_signal_bot.stable_adoption.rollback import compute_rollback_readiness, require_rollback_readiness_before_activation
from sports_signal_bot.stable_adoption.snapshots import capture_stable_reference_snapshot

def test_rollback_readiness():
    snapshot = capture_stable_reference_snapshot("adp_01", {"fam": "v1"}, ["man_01"])
    readiness = compute_rollback_readiness("adp_01", snapshot)
    assert require_rollback_readiness_before_activation(readiness) is True

def test_rollback_readiness_missing():
    readiness = compute_rollback_readiness("adp_01", None)
    assert require_rollback_readiness_before_activation(readiness) is False
