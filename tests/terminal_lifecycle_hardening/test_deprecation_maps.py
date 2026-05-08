import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    MapFamily, DeprecationSurfaceRecord, DeprecationStateRecord, StateFamily, MapStatus
)
from src.sports_signal_bot.terminal_lifecycle_hardening.deprecation_maps import build_deprecation_map

class TestDeprecationMaps(unittest.TestCase):
    def test_build_deprecation_map_caveated(self):
        surfaces = [DeprecationSurfaceRecord(surface_id="surf_1")]
        states = []
        dep_map = build_deprecation_map(MapFamily.composite_deprecation_map, surfaces, states)
        self.assertEqual(dep_map.map_status, MapStatus.map_caveated)
        self.assertEqual(len(dep_map.warnings), 1)

    def test_build_deprecation_map_verified(self):
        surfaces = [DeprecationSurfaceRecord(surface_id="surf_1")]
        states = [DeprecationStateRecord(state_id="state_1", state_family=StateFamily.frozen_supported)]
        dep_map = build_deprecation_map(MapFamily.composite_deprecation_map, surfaces, states)
        self.assertEqual(dep_map.map_status, MapStatus.map_verified)
        self.assertEqual(len(dep_map.warnings), 0)
