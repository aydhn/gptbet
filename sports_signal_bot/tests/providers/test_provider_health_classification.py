from sports_signal_bot.providers.health import (
    HealthStatus,
    ProviderHealthRecord,
    classify_provider_health,
)


def test_provider_health_classification():
    h1 = ProviderHealthRecord(provider_name="test", recent_failure_count=0)
    assert classify_provider_health(h1) == HealthStatus.HEALTHY

    h2 = ProviderHealthRecord(provider_name="test", recent_failure_count=4)
    assert classify_provider_health(h2) == HealthStatus.UNSTABLE

    h3 = ProviderHealthRecord(provider_name="test", recent_failure_count=12)
    assert classify_provider_health(h3) == HealthStatus.QUARANTINED
