import pytest
from datetime import datetime
from sports_signal_bot.ecosystem_sync.reporting import EcosystemSyncReporter
from sports_signal_bot.ecosystem_sync.contracts import EcosystemSyncRunRecord, SyncLagRecord

def test_generate_kpis():
    reporter = EcosystemSyncReporter()

    run = EcosystemSyncRunRecord(
        run_id="run_1",
        plan_id="plan_1",
        status="success",
        start_time=datetime.utcnow(),
        lag_records=[
            SyncLagRecord(lag_id="1", subscription_id="s1", lag_seconds=10, is_stale=False),
            SyncLagRecord(lag_id="2", subscription_id="s2", lag_seconds=20, is_stale=False)
        ]
    )

    kpis = reporter.generate_kpis(run, [], [])
    assert kpis["active_subscription_count"] == 2
    assert kpis["sync_success_rate"] == 1.0
    assert kpis["sync_lag_score"] == 15.0
