import pytest
from sports_signal_bot.stable_adoption.reporting import StableAdoptionReportingHooks
from sports_signal_bot.stable_adoption.contracts import StableAdoptionRecord, AdoptionStatus

def test_reporting_hooks():
    adp1 = StableAdoptionRecord(
        adoption_id="adp_01",
        handoff_id="hf_01",
        candidate_release_id="rel_01",
        activation_bridge_id="bridge_01",
        target_component_family="fam",
        adoption_scope="narrow_family",
        current_status=AdoptionStatus.POST_ACTIVATION_VERIFIED,
        proposed_stable_pointer_target="v2"
    )
    yield_val = StableAdoptionReportingHooks.calculate_activation_approval_yield([adp1])
    assert yield_val == 1.0

    clean_rate = StableAdoptionReportingHooks.calculate_post_activation_clean_rate([adp1])
    assert clean_rate == 1.0
