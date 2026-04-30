
from datetime import datetime
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord
from sports_signal_bot.reconciliation.grouping import build_reconciliation_groups

def test_build_reconciliation_groups():
    obs1 = SourceObservationRecord(
        source_observation_id="1", provider_name="A", provider_kind="P", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.9, provider_health_status="healthy", lineage_ref="ref1"
    )
    obs2 = SourceObservationRecord(
        source_observation_id="2", provider_name="B", provider_kind="S", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.8, provider_health_status="healthy", lineage_ref="ref2"
    )
    obs3 = SourceObservationRecord(
        source_observation_id="3", provider_name="A", provider_kind="P", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match2", payload={},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.9, provider_health_status="healthy", lineage_ref="ref3"
    )

    groups = build_reconciliation_groups([obs1, obs2, obs3])
    assert len(groups) == 2

    group_match1 = next(g for g in groups if g.entity_key == "match1")
    assert group_match1.source_count == 2
    assert "A" in group_match1.providers_involved
    assert "B" in group_match1.providers_involved
