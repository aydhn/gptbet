from typing import List, Dict, Any
from .contracts import (
    BaselineSnapshotRecord,
    VariantSnapshotRecord,
    BeforeAfterMetricRecord,
    ComparisonUniverseRecord
)
import uuid

def compute_before_after_metrics(baseline: BaselineSnapshotRecord, variant: VariantSnapshotRecord) -> List[BeforeAfterMetricRecord]:
    metrics = []
    all_keys = set(baseline.metrics.keys()).union(set(variant.metrics.keys()))
    for key in all_keys:
        b_val = baseline.metrics.get(key, 0.0)
        v_val = variant.metrics.get(key, 0.0)
        delta = v_val - b_val
        delta_pct = (delta / b_val * 100) if b_val != 0 else 0.0
        metrics.append(BeforeAfterMetricRecord(
            metric_name=key,
            baseline_value=b_val,
            variant_value=v_val,
            delta=delta,
            delta_percentage=delta_pct
        ))
    return metrics

def validate_comparison_universe(baseline_data: Dict[str, Any], variant_data: Dict[str, Any]) -> ComparisonUniverseRecord:
    # Dummy check for same universe
    is_identical = baseline_data.get("sample_size") == variant_data.get("sample_size")
    return ComparisonUniverseRecord(
        universe_id=f"univ_{uuid.uuid4().hex[:8]}",
        is_identical=is_identical,
        sample_size=baseline_data.get("sample_size", 0),
        caveats=[] if is_identical else ["Sample sizes do not match"]
    )
