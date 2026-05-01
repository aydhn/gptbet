import pytest
from sports_signal_bot.external_audit_exchange.manifests import generate_external_audit_manifest

def test_generate_external_audit_manifest():
    stats = {
        "exported": 5,
        "imported": 4,
        "quarantined": 1,
        "notarizations_verified": 3,
        "notarizations_unverified": 0,
        "reputation_distribution": {"excellent": 1, "adequate": 3}
    }
    manifest = generate_external_audit_manifest(stats)
    assert manifest.exported_requests == 5
    assert manifest.quarantined_responses == 1
    assert manifest.reputation_distribution["excellent"] == 1
