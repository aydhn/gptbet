import pytest
from sports_signal_bot.transparency.logs import TransparencyLogManager
from sports_signal_bot.transparency.contracts import LogFamily, EventFamily

def test_append_and_seal():
    mgr = TransparencyLogManager()
    e1 = mgr.append_transparency_entry(LogFamily.POLICY_TRANSPARENCY_LOG, EventFamily.SIGNED_POLICY_BUNDLE_PUBLISHED, "ref1", "hash1")
    e2 = mgr.append_transparency_entry(LogFamily.POLICY_TRANSPARENCY_LOG, EventFamily.CRITICAL_DECISION_PROOF_CREATED, "ref2", "hash2")

    assert e2.prior_entry_hash == e1.event_hash

    cp = mgr.seal_transparency_checkpoint(LogFamily.POLICY_TRANSPARENCY_LOG)
    assert cp.tree_size == 2
    assert cp.root_hash is not None
