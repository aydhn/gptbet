from datetime import datetime, timezone, timedelta
from sports_signal_bot.registry_conformance.contracts import BenchmarkDimensionRecord
from sports_signal_bot.registry_conformance.baselines import (
    build_treaty_benchmark_baseline,
)
from sports_signal_bot.registry_conformance.comparisons import (
    compare_treaty_to_baseline,
    summarize_benchmark_alignment,
)


def test_benchmark_comparisons():
    now = datetime.now(timezone.utc)
    dim1 = BenchmarkDimensionRecord(dimension_name="d1", description="desc")
    baseline = build_treaty_benchmark_baseline(
        "f1", "n1", ["tf1"], [dim1], now + timedelta(days=1)
    )

    treaty_data = {"dimensions": {"d1": "strong"}}
    comparison = compare_treaty_to_baseline("t1", treaty_data, baseline)

    summary = summarize_benchmark_alignment(comparison)
    assert summary["aligned_count"] == 1
    assert summary["weaker_count"] == 0
