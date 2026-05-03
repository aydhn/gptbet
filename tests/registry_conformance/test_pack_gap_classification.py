from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.contracts import (
    ConformancePackDimensionRecord,
)
from sports_signal_bot.registry_conformance.packs import build_policy_conformance_pack


def test_gap_classification():
    now = datetime.now(timezone.utc)
    dims = [ConformancePackDimensionRecord(dimension_name="d1", is_required=True)]

    # Empty evidence means missing required dimension
    pack = build_policy_conformance_pack("scope1", dims, [], now + timedelta(days=1))

    assert len(pack.missing_dimensions) == 1
    assert pack.missing_dimensions[0] == "d1"
    assert len(pack.blocking_gaps) == 1
    assert pack.conformance_status == "blocked_by_gap"
