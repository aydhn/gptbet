import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    ClosureBundleManifestRecord, DeprecationMapManifestRecord,
    MaintenanceModeManifestRecord, LongHorizonStewardshipManifestRecord
)

class TestTerminalLifecycleHardeningManifest(unittest.TestCase):
    def test_manifest_records(self):
        c_manifest = ClosureBundleManifestRecord(manifest_id="cm1")
        self.assertEqual(c_manifest.manifest_id, "cm1")

        d_manifest = DeprecationMapManifestRecord(manifest_id="dm1")
        self.assertEqual(d_manifest.manifest_id, "dm1")

        m_manifest = MaintenanceModeManifestRecord(manifest_id="mm1")
        self.assertEqual(m_manifest.manifest_id, "mm1")

        s_manifest = LongHorizonStewardshipManifestRecord(manifest_id="sm1")
        self.assertEqual(s_manifest.manifest_id, "sm1")
