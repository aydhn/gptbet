import pytest
from sports_signal_bot.expansion_governance.conflicts import detect_cross_cohort_conflicts
from sports_signal_bot.expansion_governance.contracts import ConflictSeverity

def test_detect_cross_cohort_conflicts_same_family():
    active_cohorts = [
        {"cohort_id": "c1", "cohort_family": "alias_memory"},
        {"cohort_id": "c2", "cohort_family": "alias_memory"},
        {"cohort_id": "c3", "cohort_family": "alias_memory"},
        {"cohort_id": "c4", "cohort_family": "alias_memory"}
    ]

    conflicts = detect_cross_cohort_conflicts(active_cohorts)
    assert len(conflicts) == 1
    assert conflicts[0].severity == ConflictSeverity.CRITICAL

def test_detect_cross_cohort_conflicts_alias_reconciliation():
    active_cohorts = [
        {"cohort_id": "c1", "target_component_family": "alias_memory"},
        {"cohort_id": "c2", "target_component_family": "reconciliation"}
    ]

    conflicts = detect_cross_cohort_conflicts(active_cohorts)
    assert len(conflicts) == 1
    assert conflicts[0].conflict_family == "alias_memory_and_reconciliation_scope_conflict"
    assert conflicts[0].severity == ConflictSeverity.HIGH
