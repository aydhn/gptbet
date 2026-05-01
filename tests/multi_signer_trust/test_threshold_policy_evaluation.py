from sports_signal_bot.multi_signer_trust.thresholds import evaluate_signer_count_threshold, evaluate_weighted_trust_threshold
from sports_signal_bot.multi_signer_trust.contracts import ApprovalSignerRecord, SignerTrustLevel, SignerStatus, SignerMembershipRecord

def test_signer_count_threshold():
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.ACTIVE,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    assert evaluate_signer_count_threshold([signer], 1) == True
    assert evaluate_signer_count_threshold([signer], 2) == False

def test_weighted_trust_threshold():
    assert evaluate_weighted_trust_threshold(2.5, 2.0) == True
    assert evaluate_weighted_trust_threshold(1.5, 2.0) == False
