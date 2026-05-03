from sports_signal_bot.registry_conformance.registries import build_corridor_registry
from sports_signal_bot.registry_conformance.health import compute_registry_health


def test_registry_health():
    registry = build_corridor_registry("f1", "s1")
    # Simulate issues
    registry.health_status.stale_current_count = 5
    registry = compute_registry_health(registry)

    assert registry.health_status.status == "caution"
