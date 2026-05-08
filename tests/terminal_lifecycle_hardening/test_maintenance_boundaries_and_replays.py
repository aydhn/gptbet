import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    MaintenanceBoundaryRecord, BoundaryFamily, MaintenanceReplayRecord
)

class TestMaintenanceBoundariesAndReplays(unittest.TestCase):
    def test_maintenance_boundary_record(self):
        record = MaintenanceBoundaryRecord(
            boundary_id="mb1",
            boundary_family=BoundaryFamily.runtime_boundary,
            details={"drift_acceptable": False}
        )
        self.assertEqual(record.boundary_id, "mb1")
        self.assertEqual(record.boundary_family, BoundaryFamily.runtime_boundary)
        self.assertFalse(record.details["drift_acceptable"])

    def test_maintenance_replay_record(self):
        record = MaintenanceReplayRecord(
            replay_id="mr1",
            details={"success": True}
        )
        self.assertEqual(record.replay_id, "mr1")
        self.assertTrue(record.details["success"])
