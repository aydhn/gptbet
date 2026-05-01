import pytest
from sports_signal_bot.external_audit_exchange.reporting import calculate_external_audit_kpis
from sports_signal_bot.external_audit_exchange.contracts import ExternalAuditManifest

def test_calculate_external_audit_kpis():
    manifest = ExternalAuditManifest(
        manifest_id="m1",
        exported_requests=10,
        imported_responses=10,
        quarantined_responses=2,
        notarizations_verified=8,
        notarizations_unverified=2,
        reputation_distribution={}
    )
    kpis = calculate_external_audit_kpis(manifest)
    assert kpis["quarantine_rate"] == 0.2
    assert kpis["notarization_success_rate"] == 0.8
