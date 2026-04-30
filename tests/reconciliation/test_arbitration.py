
from datetime import datetime
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord
from sports_signal_bot.reconciliation.grouping import build_reconciliation_groups
from sports_signal_bot.reconciliation.arbitration import run_arbitration

def test_arbitration_balanced_consensus():
    obs1 = SourceObservationRecord(
        source_observation_id="1", provider_name="A", provider_kind="P", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={"score": 1},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.9, provider_health_status="healthy", lineage_ref="ref1"
    )
    obs2 = SourceObservationRecord(
        source_observation_id="2", provider_name="B", provider_kind="S", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={"score": 1},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.8, provider_health_status="healthy", lineage_ref="ref2"
    )
    obs3 = SourceObservationRecord(
        source_observation_id="3", provider_name="C", provider_kind="S", data_family="fixtures",
        sport="football", entity_type="match", entity_key="match1", payload={"score": 2},
        source_snapshot_time=datetime.now(), fetched_at=datetime.now(),
        provider_quality_score=0.7, provider_health_status="healthy", lineage_ref="ref3"
    )

    groups = build_reconciliation_groups([obs1, obs2, obs3])
    group = groups[0]

    unified, conflicts, dispute = run_arbitration(group, "balanced_consensus")
    assert dispute is None
    assert len(conflicts) > 0  # score conflict between C and A/B
    assert unified.trusted_payload["score"] == 1  # 2 vs 1 vote
