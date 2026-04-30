
from datetime import datetime
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord, ReconciliationGroupRecord
from sports_signal_bot.reconciliation.conflicts import detect_conflicts

def test_detect_kickoff_time_mismatch():
    obs1 = SourceObservationRecord(
        source_observation_id="1", provider_name="A", provider_kind="P", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={"kickoff_time": "2023-10-01T15:00:00Z"},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(), provider_quality_score=0.9, provider_health_status="healthy", lineage_ref="ref1"
    )
    obs2 = SourceObservationRecord(
        source_observation_id="2", provider_name="B", provider_kind="S", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={"kickoff_time": "2023-10-01T15:15:00Z"},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(), provider_quality_score=0.8, provider_health_status="healthy", lineage_ref="ref2"
    )
    group = ReconciliationGroupRecord(
        group_id="g1", data_family="fixtures", sport="football", entity_key="match1", source_count=2, providers_involved=["A", "B"],
        reconciliation_status="pending", conflict_count=0, confidence_score=0.0, selected_consensus_strategy="none", observations=[obs1, obs2]
    )

    conflicts = detect_conflicts(group)
    assert len(conflicts) == 1
    assert conflicts[0].field_name == "kickoff_time"
    assert conflicts[0].severity == "medium"
