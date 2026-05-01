from sports_signal_bot.multi_signer_trust.signers import compute_signer_weight
from sports_signal_bot.multi_signer_trust.contracts import ApprovalSignerRecord, SignerTrustLevel, SignerStatus, SignerMembershipRecord

def test_compute_signer_weight():
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.ACTIVE,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    weight = compute_signer_weight(signer, {}, "any")
    assert weight == 1.0

def test_compute_signer_weight_revoked():
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.REVOKED,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    weight = compute_signer_weight(signer, {}, "any")
    assert weight == 0.0
