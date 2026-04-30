import pytest
from sports_signal_bot.stable_adoption.activation import build_stable_pointer_advance, commit_limited_pointer_advance, validate_post_advance_state
from sports_signal_bot.stable_adoption.contracts import AdvancementMode, StableAdoptionRecord, AdoptionStatus

def test_pointer_advancement():
    advance = build_stable_pointer_advance(
        adoption_id="adp_01",
        old_ref="v1",
        new_ref="v2",
        mode=AdvancementMode.FAMILY_SCOPED_POINTER_ADVANCE,
        rollback_target="v1",
        scope_notes=["narrow_family"]
    )
    assert advance.new_stable_pointer_ref == "v2"

    adoption = StableAdoptionRecord(
        adoption_id="adp_01",
        handoff_id="hf_01",
        candidate_release_id="rel_02",
        activation_bridge_id="br_01",
        target_component_family="fam",
        adoption_scope="narrow_family",
        current_status=AdoptionStatus.STABLE_POINTER_ADVANCE_READY,
        proposed_stable_pointer_target="v2"
    )

    updated_adoption = commit_limited_pointer_advance(adoption, advance)
    assert validate_post_advance_state(updated_adoption) is True
