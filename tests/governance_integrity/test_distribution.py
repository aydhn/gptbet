from sports_signal_bot.governance_integrity.distribution import build_distribution_package
from sports_signal_bot.governance_integrity.imports import import_distribution_bundle
from sports_signal_bot.governance_integrity.bundles import build_signed_policy_bundle
from sports_signal_bot.governance_integrity.contracts import BundleStatus

def test_distribution_import_flow():
    payload = {"rules": ["rule"]}
    bundle = build_signed_policy_bundle(payload, "fam", "1.0", "local_dev_signer")
    pkg = build_distribution_package(bundle, payload, "fake_blob")

    # Dev signer is recognized
    imported = import_distribution_bundle(pkg)
    assert imported.initial_status == BundleStatus.REVIEW_VERIFIED

    # Unknown signer -> quarantined
    pkg.packaging_record.signature_block.signer_id = "unknown_signer"
    imported_bad = import_distribution_bundle(pkg)
    assert imported_bad.initial_status == BundleStatus.QUARANTINED
