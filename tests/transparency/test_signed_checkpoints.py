import pytest
from sports_signal_bot.transparency.logs import TransparencyLogManager
from sports_signal_bot.transparency.checkpoints import CheckpointManager
from sports_signal_bot.transparency.contracts import LogFamily, EventFamily, TrustStatus

def test_sign_and_verify_checkpoint():
    log_mgr = TransparencyLogManager()
    cp_mgr = CheckpointManager()

    log_mgr.append_transparency_entry(LogFamily.SIGNER_TRUST_LOG, EventFamily.SIGNER_TRUST_CHANGED, "ref1", "hash1")
    cp = log_mgr.seal_transparency_checkpoint(LogFamily.SIGNER_TRUST_LOG)

    sig = cp_mgr.sign_checkpoint(cp, ["signer1"], "sig_block")
    assert cp.signed_checkpoint_ref == sig.signature_id

    trust_rec = cp_mgr.validate_checkpoint_trust(cp)
    assert trust_rec.trust_status == TrustStatus.TRUSTED
