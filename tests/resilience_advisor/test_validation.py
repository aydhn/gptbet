from sports_signal_bot.resilience_advisor.contracts import (
    RemediationPlaybookRecord,
    PlaybookStepRecord
)
from sports_signal_bot.resilience_advisor.validation import (
    validate_playbook_safety,
    summarize_validation_outcome
)


def test_validate_playbook_safety_all_safe():
    step1 = PlaybookStepRecord(
        step_order=1,
        step_family="isolation",
        rationale="Isolate component",
        safety_bounds="Must not drop traffic",
        success_criteria="Component isolated"
    )
    step2 = PlaybookStepRecord(
        step_order=2,
        step_family="restart",
        rationale="Restart component",
        safety_bounds="Max 10s downtime",
        success_criteria="Component restarted"
    )
    playbook = RemediationPlaybookRecord(
        playbook_id="pb-1",
        playbook_family="db-recovery",
        target_incident_family="db-lock",
        synthesized_from_pattern_refs=[],
        steps=[step1, step2],
        prerequisites=[],
        risk_notes=[],
        rollback_notes=[],
        expected_signals=[]
    )

    assert validate_playbook_safety(playbook) is True
    assert summarize_validation_outcome(playbook) == "validated_safe"


def test_validate_playbook_safety_unsafe_step():
    step1 = PlaybookStepRecord(
        step_order=1,
        step_family="isolation",
        rationale="Isolate component",
        safety_bounds="Must not drop traffic",
        success_criteria="Component isolated"
    )
    step2 = PlaybookStepRecord(
        step_order=2,
        step_family="restart",
        rationale="Restart component",
        safety_bounds="",  # Unsafe step (empty safety bounds)
        success_criteria="Component restarted"
    )
    playbook = RemediationPlaybookRecord(
        playbook_id="pb-2",
        playbook_family="db-recovery",
        target_incident_family="db-lock",
        synthesized_from_pattern_refs=[],
        steps=[step1, step2],
        prerequisites=[],
        risk_notes=[],
        rollback_notes=[],
        expected_signals=[]
    )

    assert validate_playbook_safety(playbook) is False
    assert summarize_validation_outcome(playbook) == "validation_failed"


def test_validate_playbook_safety_empty_steps():
    playbook = RemediationPlaybookRecord(
        playbook_id="pb-3",
        playbook_family="empty-playbook",
        target_incident_family="none",
        synthesized_from_pattern_refs=[],
        steps=[],
        prerequisites=[],
        risk_notes=[],
        rollback_notes=[],
        expected_signals=[]
    )

    # An empty playbook has no unsafe steps
    assert validate_playbook_safety(playbook) is True
    assert summarize_validation_outcome(playbook) == "validated_safe"
