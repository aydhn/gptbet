import unittest
from src.sports_signal_bot.terminal_lifecycle_hardening.contracts import (
    BundleFamily, SectionFamily, ClosureBundleSectionRecord, BundleStatus
)
from src.sports_signal_bot.terminal_lifecycle_hardening.closure_bundles import build_closure_bundle

class TestClosureBundles(unittest.TestCase):
    def test_build_closure_bundle_caveated(self):
        sections = [ClosureBundleSectionRecord(section_id="1", section_family=SectionFamily.terminal_summary_section)]
        bundle = build_closure_bundle(BundleFamily.composite_terminal_closure_bundle, sections)
        self.assertEqual(bundle.bundle_status, BundleStatus.bundle_caveated)
        self.assertEqual(len(bundle.warnings), 2)

    def test_build_closure_bundle_verified(self):
        sections = [
            ClosureBundleSectionRecord(section_id="1", section_family=SectionFamily.no_safe_visibility_section),
            ClosureBundleSectionRecord(section_id="2", section_family=SectionFamily.sovereignty_visibility_section)
        ]
        bundle = build_closure_bundle(BundleFamily.composite_terminal_closure_bundle, sections)
        self.assertEqual(bundle.bundle_status, BundleStatus.bundle_verified)
        self.assertEqual(len(bundle.warnings), 0)
