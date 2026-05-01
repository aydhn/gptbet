from sports_signal_bot.multi_signer_trust.thresholds import summarize_threshold_result
from sports_signal_bot.multi_signer_trust.contracts import ApprovalThresholdPolicyRecord, ApprovalSignerRecord, SignerTrustLevel, SignerStatus, SignerMembershipRecord

def test_quorum_satisfaction():
    policy = ApprovalThresholdPolicyRecord(
        threshold_policy_id="p1", policy_family="test", target_scope={},
        min_signer_count=1, min_weighted_trust=1.0, expiry_seconds=3600
    )
    signer = ApprovalSignerRecord(
        signer_id="u1", trust_level=SignerTrustLevel.HIGH, status=SignerStatus.ACTIVE,
        membership=SignerMembershipRecord(signer_id="u1", group_names=["g1"])
    )
    result = summarize_threshold_result([signer], policy, {}, [])
    assert result.signer_count_satisfied == True
    assert result.weighted_trust_satisfied == True
