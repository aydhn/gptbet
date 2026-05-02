import pytest
from sports_signal_bot.assurance.bundles import build_proof_carrying_bundle

def test_policy_bundle():
    bundle = build_proof_carrying_bundle("t1", [], ["att_1"])
    assert bundle.target_ref == "t1"
