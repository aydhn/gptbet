import pytest
from datetime import datetime, timezone, timedelta
from sports_signal_bot.overlay_mesh_governance import (
    build_baseline_registry,
    register_baseline_entry,
    validate_baseline_currentness,
    BaselineRegistryEntryRecord,
    BaselineRegistryVersionRecord,
    BaselineRegistryApplicabilityRecord,
    BaselineRegistrySupersessionRecord
)

def test_registry_currentness():
    reg = build_baseline_registry("r1", "sovereign_resilience_baseline_registry")
    now = datetime.now(timezone.utc)
    entry = BaselineRegistryEntryRecord(
        baseline_registry_entry_id="e1",
        baseline_ref="b1",
        baseline_family="f1",
        version_ref=BaselineRegistryVersionRecord(version_id="v1", timestamp=now),
        currentness_state="current",
        applicability_scope=BaselineRegistryApplicabilityRecord(applicability_scopes=["scope1"]),
        validity_window={"start": now - timedelta(days=1), "end": now - timedelta(hours=1)},
        supersession_state=BaselineRegistrySupersessionRecord(supersession_reason="none")
    )
    register_baseline_entry(reg, entry)
    state = validate_baseline_currentness(entry)
    assert state == "expired"
