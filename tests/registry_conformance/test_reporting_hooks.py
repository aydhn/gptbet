from sports_signal_bot.registry_conformance.reporting import (
    generate_registry_conformance_summary,
)


def test_reporting():
    summary = generate_registry_conformance_summary([], [], [], [])
    assert summary["summary"]["total_registries"] == 0
