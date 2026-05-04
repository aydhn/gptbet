import pytest
from datetime import datetime, timezone
from sports_signal_bot.overlay_mesh_governance import (
    BaselineRegistryEntryRecord,
    BaselineRegistryVersionRecord,
    BaselineRegistryApplicabilityRecord,
    BaselineRegistrySupersessionRecord,
    supersede_baseline_registry_entry,
    link_successor_baseline
)

def test_supersede_entry():
    now = datetime.now(timezone.utc)
    entry = BaselineRegistryEntryRecord(
        baseline_registry_entry_id="e1",
        baseline_ref="b1",
        baseline_family="f1",
        version_ref=BaselineRegistryVersionRecord(version_id="v1", timestamp=now),
        currentness_state="current",
        applicability_scope=BaselineRegistryApplicabilityRecord(applicability_scopes=["scope1"]),
        validity_window={"start": now},
        supersession_state=BaselineRegistrySupersessionRecord(supersession_reason="none")
    )
    res = supersede_baseline_registry_entry(entry, "e2", "new version")
    assert res.currentness_state == "superseded"
    assert res.supersession_state.successor_ref == "e2"

def test_link_successor():
    now = datetime.now(timezone.utc)
    entry1 = BaselineRegistryEntryRecord(
        baseline_registry_entry_id="e1",
        baseline_ref="b1",
        baseline_family="f1",
        version_ref=BaselineRegistryVersionRecord(version_id="v1", timestamp=now),
        currentness_state="current",
        applicability_scope=BaselineRegistryApplicabilityRecord(applicability_scopes=["scope1"]),
        validity_window={"start": now},
        supersession_state=BaselineRegistrySupersessionRecord(supersession_reason="none")
    )
    entry2 = BaselineRegistryEntryRecord(
        baseline_registry_entry_id="e2",
        baseline_ref="b2",
        baseline_family="f1",
        version_ref=BaselineRegistryVersionRecord(version_id="v2", timestamp=now),
        currentness_state="current",
        applicability_scope=BaselineRegistryApplicabilityRecord(applicability_scopes=["scope1"]),
        validity_window={"start": now},
        supersession_state=BaselineRegistrySupersessionRecord(supersession_reason="none")
    )
    link_successor_baseline(entry1, entry2)
    assert entry1.currentness_state == "superseded"
    assert entry1.supersession_state.successor_ref == "e2"
