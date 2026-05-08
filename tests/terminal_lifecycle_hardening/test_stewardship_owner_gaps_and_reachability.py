import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    StewardshipGapRecord, StewardshipReachabilityRecord
)

class TestStewardshipOwnerGapsAndReachability(unittest.TestCase):
    def test_stewardship_gap_record(self):
        record = StewardshipGapRecord(
            gap_id="sg1",
            details={"missing_escalation": True}
        )
        self.assertEqual(record.gap_id, "sg1")
        self.assertTrue(record.details["missing_escalation"])

    def test_stewardship_reachability_record(self):
        record = StewardshipReachabilityRecord(
            reachability_id="sr1",
            details={"reachable_in_24h": True}
        )
        self.assertEqual(record.reachability_id, "sr1")
        self.assertTrue(record.details["reachable_in_24h"])
