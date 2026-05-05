import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    ConcurrencyRegressionRecord, ConcurrencyBaselineRecord,
    ConcurrencyComparisonRecord, ConcurrencyImpactRecord,
    ConcurrencySeverityRecord, ConcurrencyRegressionHealthRecord,
    ConcurrencyRegressionManifestRecord, ConcurrencyRegressionWarningRecord
)

def compare_concurrency_baselines(baseline: ConcurrencyBaselineRecord, current: ConcurrencyComparisonRecord) -> List[str]:
    """Compares baseline and current metrics to find regressions."""
    regressions = []
    for metric, base_val in baseline.metrics.items():
        curr_val = current.metrics.get(metric)
        if curr_val is not None:
            # Assuming lower is better for concurrency metrics (e.g., race counts, drift ms)
            if curr_val > base_val:
                regressions.append(metric)
    return regressions

def classify_concurrency_regression(metric: str, base_val: float, curr_val: float) -> ConcurrencySeverityRecord:
    """Classifies the severity of a regression."""
    diff = curr_val - base_val
    level = "info"

    if "race" in metric.lower() and diff > 0:
        level = "release_blocking"
    elif "drift" in metric.lower() or "stale" in metric.lower():
        level = "high"
    elif "ordering" in metric.lower():
        level = "high"
    elif diff > base_val * 0.5: # 50% worse
        level = "medium"
    else:
        level = "low"

    return ConcurrencySeverityRecord(
        severity_id=f"sev_{uuid.uuid4().hex[:8]}",
        level=level
    )

def detect_concurrency_regressions(
    baseline: ConcurrencyBaselineRecord,
    current: ConcurrencyComparisonRecord
) -> List[ConcurrencyRegressionRecord]:
    """Detects concurrency regressions."""
    records = []
    metrics_with_regression = compare_concurrency_baselines(baseline, current)

    for metric in metrics_with_regression:
        severity = classify_concurrency_regression(metric, baseline.metrics[metric], current.metrics[metric])

        record = ConcurrencyRegressionRecord(
            regression_id=f"reg_{uuid.uuid4().hex[:8]}",
            baseline_ref=baseline.baseline_id,
            comparison_ref=current.comparison_id,
            impact_ref=f"imp_{uuid.uuid4().hex[:8]}",
            severity_ref=severity.severity_id,
            status="regression_detected",
            warnings=[
                ConcurrencyRegressionWarningRecord(
                    warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                    message=f"Regression detected in {metric}: {baseline.metrics[metric]} -> {current.metrics[metric]}",
                    severity=severity.level
                )
            ]
        )
        records.append(record)

    return records

def summarize_concurrency_regressions(regressions: List[ConcurrencyRegressionRecord]) -> ConcurrencyRegressionManifestRecord:
    """Summarizes concurrency regressions."""
    blocking = sum(1 for r in regressions if any(w.severity == "release_blocking" for w in r.warnings))

    health = ConcurrencyRegressionHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=blocking == 0,
        status_summary=f"Found {len(regressions)} regressions, {blocking} are release blocking."
    )

    return ConcurrencyRegressionManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        regressions=regressions,
        health=health
    )
