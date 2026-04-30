import pytest
from sports_signal_bot.stable_adoption.blockers import detect_adoption_conflicts
from sports_signal_bot.stable_adoption.contracts import StableAdoptionRecord, AdoptionStatus

def test_detect_conflicts():
    adp1 = StableAdoptionRecord(
        adoption_id="adp_01",
        handoff_id="hf_01",
        candidate_release_id="rel_01",
        activation_bridge_id="bridge_01",
        target_component_family="fam",
        adoption_scope="narrow_family",
        current_status=AdoptionStatus.PENDING_ACTIVATION_COUNCIL,
        proposed_stable_pointer_target="v2"
    )
    adp2 = StableAdoptionRecord(
        adoption_id="adp_02",
        handoff_id="hf_02",
        candidate_release_id="rel_02",
        activation_bridge_id="bridge_02",
        target_component_family="fam",
        adoption_scope="narrow_family",
        current_status=AdoptionStatus.PENDING_ACTIVATION_COUNCIL,
        proposed_stable_pointer_target="v3"
    )
    conflicts = detect_adoption_conflicts("adp_01", [adp1, adp2])
    assert len(conflicts) == 1
    assert conflicts[0].blocker_family == "family_freeze_active"
