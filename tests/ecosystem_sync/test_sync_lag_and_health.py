from datetime import datetime, timedelta, timezone

from sports_signal_bot.ecosystem_sync.checkpoints import (
    classify_sync_health,
    create_sync_checkpoint,
    detect_stale_subscriptions,
)
from sports_signal_bot.ecosystem_sync.lag import compute_sync_lag


def test_compute_sync_lag():
    chk = create_sync_checkpoint("source_1", "local_1", "hash1", "hash2")
    # Simulate time passing
    future_time = chk.local.timestamp + timedelta(seconds=100)

    lag = compute_sync_lag(chk, future_time)
    assert lag.lag_seconds == 100
    assert lag.is_stale is False

    very_future_time = chk.local.timestamp + timedelta(days=2)
    lag2 = compute_sync_lag(chk, very_future_time)
    assert lag2.is_stale is True


def test_detect_stale_subscriptions():
    chk = create_sync_checkpoint("source_1", "local_1", "hash1", "hash2")
    # artificially age the checkpoint
    chk.local.timestamp = datetime.now(timezone.utc) - timedelta(seconds=200)

    stale_records = detect_stale_subscriptions([chk], threshold_seconds=100)
    assert len(stale_records) == 1
    assert stale_records[0].is_stale is True

    health = classify_sync_health(stale_records)
    assert health.status == "unhealthy"
