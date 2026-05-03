from datetime import datetime, timezone
import uuid
from typing import List
from .contracts import (
    TreatyBenchmarkBaselineRecord,
    BenchmarkDimensionRecord,
    BenchmarkBaselineVersionRecord,
    EntrySemanticVersionRecord,
    RegistryFreshnessRecord,
)


def build_treaty_benchmark_baseline(
    baseline_family: str,
    baseline_name: str,
    applicable_treaty_families: List[str],
    dimensions: List[BenchmarkDimensionRecord],
    valid_until: datetime,
) -> TreatyBenchmarkBaselineRecord:
    now = datetime.now(timezone.utc)

    version = BenchmarkBaselineVersionRecord(
        version_id=f"v_{uuid.uuid4().hex[:8]}",
        semantic_version=EntrySemanticVersionRecord(major=1, minor=0, patch=0),
    )

    freshness = RegistryFreshnessRecord(
        last_verified_at=now, valid_until=valid_until, is_stale=False
    )

    return TreatyBenchmarkBaselineRecord(
        baseline_id=f"baseline_{uuid.uuid4().hex[:8]}",
        baseline_family=baseline_family,
        baseline_name=baseline_name,
        applicable_treaty_families=applicable_treaty_families,
        dimension_refs=dimensions,
        version_ref=version,
        freshness_state=freshness,
        intended_use_scope="general_comparison",
    )
