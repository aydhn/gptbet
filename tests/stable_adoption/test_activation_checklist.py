import pytest
from sports_signal_bot.stable_adoption.checklists import build_activation_checklist, validate_activation_checklist

def test_activation_checklist():
    checklist = build_activation_checklist(
        adoption_id="adp_01",
        handoff_evidence_present=True,
        approvals_complete=True,
        rollback_target_known=True,
        docs_linked=True,
        post_activation_plan_ready=True,
        no_blockers=True
    )
    assert validate_activation_checklist(checklist) is True

    incomplete_checklist = build_activation_checklist(
        adoption_id="adp_02",
        handoff_evidence_present=True,
        approvals_complete=False,
        rollback_target_known=True,
        docs_linked=True,
        post_activation_plan_ready=True,
        no_blockers=True
    )
    assert validate_activation_checklist(incomplete_checklist) is False
