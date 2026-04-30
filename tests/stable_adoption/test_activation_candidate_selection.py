import pytest
from sports_signal_bot.stable_adoption.contracts import StableAdoptionRecord, AdoptionStatus

def test_stable_adoption_record_creation():
    record = StableAdoptionRecord(
        adoption_id="adp_01",
        handoff_id="hf_01",
        candidate_release_id="rel_01",
        activation_bridge_id="bridge_01",
        target_component_family="provider_priority",
        adoption_scope="narrow_family",
        current_status=AdoptionStatus.ADOPTION_CANDIDATE_IDENTIFIED,
        proposed_stable_pointer_target="ptr_target"
    )
    assert record.adoption_id == "adp_01"
    assert record.current_status == AdoptionStatus.ADOPTION_CANDIDATE_IDENTIFIED
