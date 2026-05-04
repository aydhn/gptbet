from sports_signal_bot.governance_recovery.exception_federations import (
    build_exception_registry_federation,
    summarize_exception_federation_health
)

def test_build_exception_registry_federation():
    fed = build_exception_registry_federation("fed_1", "review_only_exception_federation")
    assert fed.exception_federation_id == "fed_1"
    assert fed.health_status.is_healthy is True

def test_summarize_exception_federation_health():
    fed = build_exception_registry_federation("fed_1", "review_only_exception_federation")
    health = summarize_exception_federation_health(fed)
    assert health.is_healthy is True
