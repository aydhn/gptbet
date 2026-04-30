
from sports_signal_bot.reconciliation.contracts import FieldConflictRecord
from sports_signal_bot.reconciliation.confidence import compute_field_confidence

def test_compute_field_confidence():
    # No conflicts
    assert compute_field_confidence([]) == 1.0

    # Medium conflict
    c1 = FieldConflictRecord(conflict_id="1", group_id="g1", field_name="time", severity="medium", conflict_type="mismatch", values={})
    assert compute_field_confidence([c1]) == 0.7

    # Critical conflict
    c2 = FieldConflictRecord(conflict_id="2", group_id="g1", field_name="status", severity="critical", conflict_type="mismatch", values={})
    assert abs(compute_field_confidence([c2]) - 0.1) < 1e-6
