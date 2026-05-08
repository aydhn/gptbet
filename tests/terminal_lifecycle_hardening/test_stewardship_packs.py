import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    PackFamily, StewardshipOwnerRecord, OwnerFamily, PackStatus
)
from src.sports_signal_bot.terminal_lifecycle_hardening.stewardship_packs import build_long_horizon_stewardship_pack

class TestStewardshipPacks(unittest.TestCase):
    def test_build_long_horizon_stewardship_pack_caveated(self):
        owners = []
        pack = build_long_horizon_stewardship_pack(PackFamily.composite_long_horizon_stewardship_pack, owners)
        self.assertEqual(pack.pack_status, PackStatus.pack_caveated)
        self.assertEqual(len(pack.warnings), 1)

    def test_build_long_horizon_stewardship_pack_verified(self):
        owners = [StewardshipOwnerRecord(owner_id="o1", owner_family=OwnerFamily.runtime_owner)]
        pack = build_long_horizon_stewardship_pack(PackFamily.composite_long_horizon_stewardship_pack, owners)
        self.assertEqual(pack.pack_status, PackStatus.pack_verified)
        self.assertEqual(len(pack.warnings), 0)
