from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.registries import build_corridor_registry
from sports_signal_bot.registry_conformance.packs import build_policy_conformance_pack
from sports_signal_bot.registry_conformance.projections import (
    inject_registry_and_pack_factors,
)


def test_scorecard_projection():
    now = datetime.now(timezone.utc)
    registry = build_corridor_registry("f1", "s1")
    pack = build_policy_conformance_pack("scope1", [], [], now + timedelta(days=1))

    base_scorecard = {"base_score": 90}
    projected = inject_registry_and_pack_factors(base_scorecard, registry, pack)

    assert "registry_health_contribution" in projected
    assert "conformance_pack_contribution" in projected
    assert "adjusted_interoperability_score" in projected
