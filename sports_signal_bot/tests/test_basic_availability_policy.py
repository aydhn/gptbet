from sports_signal_bot.source_selection.contracts import (
    SourceEligibilityRecord,
    SourcePolicyDefinition,
)
from sports_signal_bot.source_selection.metadata import SourceMetadataRecord
from sports_signal_bot.source_selection.policies import BasicAvailabilityPolicy


def test_basic_availability_policy_missing_prediction():
    policy = BasicAvailabilityPolicy(
        SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy")
    )
    meta = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        is_prediction_available=False,
    )
    elig = SourceEligibilityRecord(
        event_id="e",
        sport="s",
        market_type="m",
        source_name="s",
        source_family="f",
        is_eligible=True,
    )

    policy.evaluate(meta, elig, {})

    assert not elig.is_available
    assert not elig.is_eligible
    assert any(ex.reason_code == "source_unavailable" for ex in elig.exclusion_reasons)


def test_basic_availability_policy_invalid_probabilities():
    policy = BasicAvailabilityPolicy(
        SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy")
    )
    meta = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        is_prediction_available=True,
        has_invalid_probabilities=True,
    )
    elig = SourceEligibilityRecord(
        event_id="e",
        sport="s",
        market_type="m",
        source_name="s",
        source_family="f",
        is_eligible=True,
    )

    policy.evaluate(meta, elig, {})

    assert not elig.is_eligible
    assert any(
        ex.reason_code == "invalid_probabilities" for ex in elig.exclusion_reasons
    )
