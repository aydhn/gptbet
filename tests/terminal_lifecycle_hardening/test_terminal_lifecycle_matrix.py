import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import LifecycleMatrixRow
from src.sports_signal_bot.terminal_lifecycle_hardening.summaries import validate_terminal_lifecycle_row, build_terminal_lifecycle_matrix, summarize_terminal_lifecycle_matrix

class TestTerminalLifecycleMatrix(unittest.TestCase):
    def test_validate_row_success(self):
        row = LifecycleMatrixRow(
            surface_id="surf_1", owner_visible=True, freshness_note_visible=True,
            no_safe_visible=True, sovereignty_note_visible=True, residue_visible=True,
            degraded_lane_visible=True, replayability_preserved=True, lineage_preserved=True,
            rollback_explicit=True, deprecation_state_explicit=True, maintenance_boundary_explicit=True,
            stewardship_cadence_explicit=True, acceptance_carry_forward_explicit=True
        )
        self.assertTrue(validate_terminal_lifecycle_row(row))

    def test_validate_row_fail(self):
        row = LifecycleMatrixRow(
            surface_id="surf_2", owner_visible=True, freshness_note_visible=False, # <-- Fail
            no_safe_visible=True, sovereignty_note_visible=True, residue_visible=True,
            degraded_lane_visible=True, replayability_preserved=True, lineage_preserved=True,
            rollback_explicit=True, deprecation_state_explicit=True, maintenance_boundary_explicit=True,
            stewardship_cadence_explicit=True, acceptance_carry_forward_explicit=True
        )
        self.assertFalse(validate_terminal_lifecycle_row(row))

    def test_summarize_matrix(self):
        rows = [
            LifecycleMatrixRow(
                surface_id="surf_1", owner_visible=True, freshness_note_visible=True,
                no_safe_visible=True, sovereignty_note_visible=True, residue_visible=True,
                degraded_lane_visible=True, replayability_preserved=True, lineage_preserved=True,
                rollback_explicit=True, deprecation_state_explicit=True, maintenance_boundary_explicit=True,
                stewardship_cadence_explicit=True, acceptance_carry_forward_explicit=True
            ),
            LifecycleMatrixRow(surface_id="surf_2") # All false by default
        ]

        summary = summarize_terminal_lifecycle_matrix(rows)
        self.assertEqual(summary["total_rows"], 2)
        self.assertEqual(summary["valid_rows"], 1)
        self.assertEqual(summary["invalid_rows"], 1)
