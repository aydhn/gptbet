from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.entries import build_registry_entry
from sports_signal_bot.registry_conformance.currentness import (
    compute_currentness,
    supersede_registry_entry,
)
from sports_signal_bot.registry_conformance.registries import (
    build_corridor_registry,
    register_registry_entry,
)


def test_entry_currentness():
    now = datetime.now(timezone.utc)
    from sports_signal_bot.registry_conformance.contracts import VersionLineageRecord

    entry = build_registry_entry(
        "corridor_entry", "t1", "v1", VersionLineageRecord(), now + timedelta(days=1)
    )

    # State is drafted by default
    decision = compute_currentness(entry)
    assert not decision.is_current

    entry.state_ref.state = "current"
    decision = compute_currentness(entry)
    assert decision.is_current

    # Supersede
    superseded_entry = supersede_registry_entry(entry, "entry2", "expired_treaty")
    decision = compute_currentness(superseded_entry)
    assert not decision.is_current
    assert superseded_entry.supersession_state is not None
