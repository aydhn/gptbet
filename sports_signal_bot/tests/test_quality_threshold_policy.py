from sports_signal_bot.source_selection.metadata import SourceMetadataRecord
from sports_signal_bot.source_selection.contracts import SourceEligibilityRecord, SourcePolicyDefinition, SourceTrustScoreRecord
from sports_signal_bot.source_selection.policies import QualityThresholdPolicy

def test_quality_threshold_low_trust():
    defn = SourcePolicyDefinition(policy_name="QualityThresholdPolicy", parameters={"min_trust_score": 0.5})
    policy = QualityThresholdPolicy(defn)

    meta = SourceMetadataRecord(source_name="s", event_id="e", sport="s", market_type="m")
    elig = SourceEligibilityRecord(event_id="e", sport="s", market_type="m", source_name="s", source_family="f", is_eligible=True)
    elig.trust_score = SourceTrustScoreRecord(total_trust_score=0.4)

    policy.evaluate(meta, elig, {})

    assert not elig.is_eligible
    assert any(ex.reason_code == "low_trust_score" for ex in elig.exclusion_reasons)
