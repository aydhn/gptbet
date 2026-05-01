import pytest
from sports_signal_bot.transparency.logs import TransparencyLogManager
from sports_signal_bot.transparency.mirrors import MirrorManager
from sports_signal_bot.transparency.contracts import LogFamily, EventFamily, TrustStatus, VerificationStatus

def test_mirror_sync_and_verify():
    log_mgr = TransparencyLogManager()
    mirror_mgr = MirrorManager()

    log_mgr.append_transparency_entry(LogFamily.GOVERNANCE_DECISION_LOG, EventFamily.CRITICAL_DECISION_PROOF_CREATED, "ref1", "hash1")
    cp1 = log_mgr.seal_transparency_checkpoint(LogFamily.GOVERNANCE_DECISION_LOG)

    mirror = mirror_mgr.create_verification_mirror("decision_mirror", cp1.log_id)
    assert mirror.trust_status == TrustStatus.REVIEW_REQUIRED

    mirror_mgr.sync_mirror_from_source(mirror.mirror_id, cp1)

    ver = mirror_mgr.verify_mirror_checkpoint(mirror.mirror_id, cp1)
    assert ver.status == VerificationStatus.VERIFIED

    # Simulate an outdated mirror checking a newer checkpoint
    log_mgr.append_transparency_entry(LogFamily.GOVERNANCE_DECISION_LOG, EventFamily.CRITICAL_DECISION_PROOF_CREATED, "ref2", "hash2")
    cp2 = log_mgr.seal_transparency_checkpoint(LogFamily.GOVERNANCE_DECISION_LOG)

    ver2 = mirror_mgr.verify_mirror_checkpoint(mirror.mirror_id, cp2)
    assert ver2.status == VerificationStatus.FAILED
    assert mirror.trust_status == TrustStatus.QUARANTINED
