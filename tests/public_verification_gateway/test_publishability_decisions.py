from datetime import datetime
from src.sports_signal_bot.public_verification_gateway.contracts import DisclosureBundleRecord
from src.sports_signal_bot.public_verification_gateway.publication import evaluate_publishability
from src.sports_signal_bot.public_verification_gateway.profiles import get_default_profiles

def test_publishability_decision():
    profile = get_default_profiles()[0] # public_minimal
    bundle = DisclosureBundleRecord(
        disclosure_bundle_id="b1",
        bundle_family="policy_bundle_disclosure",
        publication_profile="public_minimal",
        source_refs=[],
        included_items=[],
        redaction_profile="strict",
        verification_refs=["proof1"],
        publishability_status="draft",
        created_at=datetime.utcnow()
    )

    payload = {"safe": "value"}
    decision = evaluate_publishability(bundle, payload, profile)
    assert decision.decision == "publish_ready"
