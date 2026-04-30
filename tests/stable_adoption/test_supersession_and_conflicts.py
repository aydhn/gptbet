import pytest
from sports_signal_bot.stable_adoption.blockers import detect_superseding_adoption
from sports_signal_bot.stable_adoption.contracts import StableAdoptionRecord, AdoptionStatus

def test_detect_superseding():
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
    blocker = detect_superseding_adoption("adp_01", "rel_01", [adp1, adp2])
    assert blocker is not None
    assert blocker.blocker_family == "superseded_candidate"
