from sports_signal_bot.multi_signer_trust.thresholds import evaluate_mandatory_presence
from sports_signal_bot.multi_signer_trust.contracts import MandatoryPresenceRuleRecord, ApprovalSignerRecord, SignerTrustLevel, SignerStatus, SignerMembershipRecord

def test_mandatory_presence():
    rule = MandatoryPresenceRuleRecord(required_group="g1", min_count=1)
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.ACTIVE,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    assert evaluate_mandatory_presence([signer], [rule]) == True

    rule2 = MandatoryPresenceRuleRecord(required_group="g2", min_count=1)
    assert evaluate_mandatory_presence([signer], [rule2]) == False
