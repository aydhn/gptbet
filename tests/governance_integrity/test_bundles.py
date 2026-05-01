from sports_signal_bot.governance_integrity.bundles import build_signed_policy_bundle
from sports_signal_bot.governance_integrity.verification import run_integrity_verification

def test_build_and_verify_bundle():
    payload = {"rules": ["no_growth"]}
    bundle = build_signed_policy_bundle(
        payload=payload,
        bundle_family="growth_rules",
        bundle_version="1.0",
        signer_id="local_dev_signer"
    )

    assert bundle.signed_bundle_id.startswith("bundle_")

    # Verify
    res = run_integrity_verification(bundle, payload)
    assert res["is_valid"] is True
