from sports_signal_bot.providers.contracts import DataFamily
from sports_signal_bot.providers.manifests import build_provider_manifest
from sports_signal_bot.providers.requests import ProviderRequestRecord


def test_provider_manifest():
    req = ProviderRequestRecord(sport="football", data_family=DataFamily.FIXTURES)
    manifest = build_provider_manifest(
        req, "test_provider", ["test_provider"], 10, 0.95
    )
    assert manifest.final_provider == "test_provider"
    assert manifest.record_count == 10
