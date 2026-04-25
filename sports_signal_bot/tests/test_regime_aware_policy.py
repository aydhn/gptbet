from sports_signal_bot.source_selection.metadata import SourceMetadataRecord
from sports_signal_bot.source_selection.contracts import SourceEligibilityRecord, SourcePolicyDefinition, SourceTrustScoreRecord
from sports_signal_bot.source_selection.policies import RegimeAwarePolicy

def test_regime_aware_policy():
    policy = RegimeAwarePolicy(SourcePolicyDefinition(policy_name="RegimeAwarePolicy"))

    meta = SourceMetadataRecord(source_name="s", event_id="e", sport="s", market_type="m")
    elig = SourceEligibilityRecord(event_id="e", sport="s", market_type="m", source_name="s", source_family="f", is_eligible=True)
    elig.trust_score = SourceTrustScoreRecord(total_trust_score=0.8, regime_fit_score=0.1)

    policy.evaluate(meta, elig, {})

    assert not elig.is_eligible
    assert any(ex.reason_code == "low_regime_evidence" for ex in elig.exclusion_reasons)
