from datetime import datetime, timezone
import uuid
from typing import List, Dict
from .contracts import (
    TreatyBenchmarkBaselineRecord,
    BenchmarkComparisonRecord,
    BenchmarkDeviationRecord,
    BenchmarkCaveatRecord,
)


def compute_benchmark_deviations(
    target_treaty_data: Dict, baseline: TreatyBenchmarkBaselineRecord
) -> List[BenchmarkDeviationRecord]:
    deviations = []

    # Simple mock deviation logic for demonstration
    treaty_dims = target_treaty_data.get("dimensions", {})

    for dim in baseline.dimension_refs:
        if dim.dimension_name not in treaty_dims:
            deviations.append(
                BenchmarkDeviationRecord(
                    deviation_type="missing_dimension",
                    dimension_ref=dim.dimension_name,
                    description=f"Treaty missing required dimension: {dim.dimension_name}",
                )
            )
        else:
            treaty_val = treaty_dims[dim.dimension_name]
            # Mock check: if treaty_val is 'weak', it's weaker
            if treaty_val == "weak":
                deviations.append(
                    BenchmarkDeviationRecord(
                        deviation_type="weaker_than_baseline",
                        dimension_ref=dim.dimension_name,
                        description=f"Treaty is weaker than baseline for: {dim.dimension_name}",
                    )
                )
            elif treaty_val == "strong":
                deviations.append(
                    BenchmarkDeviationRecord(
                        deviation_type="stronger_than_baseline",
                        dimension_ref=dim.dimension_name,
                        description=f"Treaty is stronger than baseline for: {dim.dimension_name}",
                    )
                )
            else:
                deviations.append(
                    BenchmarkDeviationRecord(
                        deviation_type="aligned_with_baseline",
                        dimension_ref=dim.dimension_name,
                        description=f"Treaty is aligned with baseline for: {dim.dimension_name}",
                    )
                )

    return deviations


def compare_treaty_to_baseline(
    target_treaty_ref: str,
    target_treaty_data: Dict,
    baseline: TreatyBenchmarkBaselineRecord,
) -> BenchmarkComparisonRecord:
    deviations = compute_benchmark_deviations(target_treaty_data, baseline)
    caveats = []

    now = datetime.now(timezone.utc)
    if baseline.freshness_state.valid_until < now:
        caveats.append(
            BenchmarkCaveatRecord(
                caveat_code="STALE_BASELINE",
                description="Comparison was made against a stale baseline.",
            )
        )

    return BenchmarkComparisonRecord(
        comparison_id=f"comp_{uuid.uuid4().hex[:8]}",
        target_treaty_ref=target_treaty_ref,
        baseline_ref=baseline.baseline_id,
        deviations=deviations,
        caveats=caveats,
        computed_at=now,
    )


def summarize_benchmark_alignment(comparison: BenchmarkComparisonRecord) -> dict:
    aligned = sum(
        1
        for d in comparison.deviations
        if d.deviation_type in ["aligned_with_baseline", "stronger_than_baseline"]
    )
    missing = sum(
        1 for d in comparison.deviations if d.deviation_type == "missing_dimension"
    )
    weaker = sum(
        1
        for d in comparison.deviations
        if d.deviation_type in ["weaker_than_baseline", "narrower_than_baseline"]
    )

    return {
        "comparison_id": comparison.comparison_id,
        "total_dimensions_evaluated": len(comparison.deviations),
        "aligned_count": aligned,
        "missing_count": missing,
        "weaker_count": weaker,
        "caveat_count": len(comparison.caveats),
    }
