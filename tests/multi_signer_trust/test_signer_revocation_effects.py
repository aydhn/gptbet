from sports_signal_bot.multi_signer_trust.signers import compute_signer_weight
from sports_signal_bot.multi_signer_trust.contracts import ApprovalSignerRecord, SignerTrustLevel, SignerStatus, SignerMembershipRecord

def test_revoked_signer_weight_zero():
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.REVOKED,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    assert compute_signer_weight(signer, {}, "any") == 0.0
