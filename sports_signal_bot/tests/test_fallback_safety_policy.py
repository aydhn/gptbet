from sports_signal_bot.source_selection.contracts import (
    SourceEligibilityRecord, SourceExclusionReasonRecord,
    SourcePolicyDefinition)
from sports_signal_bot.source_selection.policies import FallbackSafetyPolicy


def test_fallback_safety_policy():
    defn = SourcePolicyDefinition(
        policy_name="FallbackSafetyPolicy",
        parameters={
            "minimum_eligible_sources": 1,
            "fallback_source_priority": ["fallback_model"],
        },
    )
    policy = FallbackSafetyPolicy(defn)

    elig = SourceEligibilityRecord(
        event_id="e",
        sport="s",
        market_type="m",
        source_name="fallback_model",
        source_family="f",
        is_eligible=False,
    )
    elig.exclusion_reasons.append(
        SourceExclusionReasonRecord(reason_code="low_trust_score", details="")
    )

    context = {}
    policy.evaluate_group([elig], context)

    assert elig.is_eligible
    assert context.get("fallback_used") is True
    assert any("Rescued" in w for w in elig.warnings)


def test_fallback_safety_policy_fatal_not_rescued():
    defn = SourcePolicyDefinition(
        policy_name="FallbackSafetyPolicy",
        parameters={
            "minimum_eligible_sources": 1,
            "fallback_source_priority": ["fallback_model"],
        },
    )
    policy = FallbackSafetyPolicy(defn)

    elig = SourceEligibilityRecord(
        event_id="e",
        sport="s",
        market_type="m",
        source_name="fallback_model",
        source_family="f",
        is_eligible=False,
    )
    elig.exclusion_reasons.append(
        SourceExclusionReasonRecord(reason_code="invalid_probabilities", details="")
    )

    context = {}
    policy.evaluate_group([elig], context)

    assert not elig.is_eligible
