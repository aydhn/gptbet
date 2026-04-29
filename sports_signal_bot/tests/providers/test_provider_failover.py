from sports_signal_bot.providers.failover import ProviderFailoverEngine, should_failover
from sports_signal_bot.providers.responses import (
    ProviderQualityRecord,
    ProviderResponseRecord,
)


def test_provider_failover():
    engine = ProviderFailoverEngine({"failover_sequences": {"primary": ["fallback_1"]}})
    assert engine.get_next_provider("primary", 0) == "fallback_1"
    assert engine.get_next_provider("primary", 1) is None

    res = ProviderResponseRecord(
        provider_used="primary",
        quality_summary=ProviderQualityRecord(is_acceptable=False),
    )
    assert should_failover(res) == True
