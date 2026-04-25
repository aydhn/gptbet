from sports_signal_bot.source_selection.metadata import SourceMetadataRecord
from sports_signal_bot.source_selection.contracts import SourceEligibilityRecord, SourcePolicyDefinition
from sports_signal_bot.source_selection.policies import PreferredCalibratedPolicy

def test_preferred_calibrated_policy():
    policy = PreferredCalibratedPolicy(SourcePolicyDefinition(policy_name="PreferredCalibratedPolicy"))

    meta1 = SourceMetadataRecord(source_name="raw", event_id="e", sport="s", market_type="m", is_calibrated=False)
    meta2 = SourceMetadataRecord(source_name="cal", event_id="e", sport="s", market_type="m", is_calibrated=True)

    elig1 = SourceEligibilityRecord(event_id="e", sport="s", market_type="m", source_name="raw", source_family="family_A", is_eligible=True)
    elig2 = SourceEligibilityRecord(event_id="e", sport="s", market_type="m", source_name="cal", source_family="family_A", is_eligible=True)

    context = {'metadata_map': {"raw": meta1, "cal": meta2}}
    policy.evaluate_group([elig1, elig2], context)

    assert not elig1.is_eligible
    assert any(ex.reason_code == "replaced_by_calibrated_variant" for ex in elig1.exclusion_reasons)
    assert elig2.is_eligible
