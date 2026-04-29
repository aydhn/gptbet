from sports_signal_bot.providers.lineage import generate_lineage_artifact
from sports_signal_bot.providers.responses import ProviderLineageRecord


def test_provider_lineage():
    record = ProviderLineageRecord(provider_used="test")
    art = generate_lineage_artifact(record)
    assert art["provider_used"] == "test"
