import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    ModeFamily, MaintenanceBoundaryRecord, BoundaryFamily, ModeStatus
)
from src.sports_signal_bot.terminal_lifecycle_hardening.maintenance_modes import build_maintenance_mode

class TestMaintenanceModes(unittest.TestCase):
    def test_build_maintenance_mode_caveated(self):
        boundaries = []
        mode = build_maintenance_mode(ModeFamily.composite_maintenance_mode, boundaries)
        self.assertEqual(mode.mode_status, ModeStatus.mode_caveated)
        self.assertEqual(len(mode.warnings), 1)

    def test_build_maintenance_mode_verified(self):
        boundaries = [MaintenanceBoundaryRecord(boundary_id="b1", boundary_family=BoundaryFamily.runtime_boundary)]
        mode = build_maintenance_mode(ModeFamily.composite_maintenance_mode, boundaries)
        self.assertEqual(mode.mode_status, ModeStatus.mode_verified)
        self.assertEqual(len(mode.warnings), 0)
