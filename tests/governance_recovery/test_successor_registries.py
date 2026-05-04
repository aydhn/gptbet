from sports_signal_bot.governance_recovery.successor_registries import (
    build_successor_registry,
    register_successor_entry
)
from sports_signal_bot.governance_recovery.contracts import SuccessorRegistryEntryRecord, SuccessorStatus

def test_build_successor_registry():
    registry = build_successor_registry("reg_1", "sovereign_baseline_successor_registry")
    assert registry.successor_registry_id == "reg_1"
    assert registry.health_status.is_healthy is True

def test_register_successor_entry():
    registry = build_successor_registry("reg_1", "sovereign_baseline_successor_registry")
    entry = SuccessorRegistryEntryRecord(
        successor_entry_id="e1", source_baseline_ref="b1", applicability_scope="all", freshness_state="fresh", successor_status=SuccessorStatus.SUCCESSOR_RESOLVED_CURRENT
    )
    registry = register_successor_entry(registry, entry)
    assert "e1" in registry.current_successor_refs
