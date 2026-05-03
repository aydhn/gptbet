from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.contracts import (
    ConformancePackDimensionRecord,
    ConformancePackEvidenceRecord,
)
from sports_signal_bot.registry_conformance.packs import (
    build_policy_conformance_pack,
    summarize_conformance_pack,
)


def test_conformance_packs():
    now = datetime.now(timezone.utc)
    dims = [ConformancePackDimensionRecord(dimension_name="d1", is_required=True)]
    evidence = [
        ConformancePackEvidenceRecord(
            evidence_id="e1", evidence_type="d1", reference_uri="uri"
        )
    ]

    pack = build_policy_conformance_pack(
        "scope1", dims, evidence, now + timedelta(days=1)
    )
    summary = summarize_conformance_pack(pack)

    assert summary["status"] == "conformant"
    assert summary["missing_count"] == 0
