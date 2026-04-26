from datetime import datetime, timedelta, timezone

from sports_signal_bot.source_selection.metadata import (
    RefreshMetadata,
    SourceMetadataRecord,
)


def test_staleness_age_calculation():
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=10)

    meta = SourceMetadataRecord(
        source_name="s",
        event_id="e",
        sport="s",
        market_type="m",
        refresh_info=RefreshMetadata(last_model_refresh_timestamp=old.isoformat()),
    )

    assert 9.9 < meta.model_age_days < 10.1
    assert meta.calibration_age_days == 999.0
