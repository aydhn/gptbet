import json
from datetime import datetime
from typing import Any, Dict, List

from sports_signal_bot.reporting.contracts import (MetricLineageRecord,
                                                   MetricValueRecord)


def build_metric_lineage(
    source_manifests: List[str],
    input_summaries: List[str],
    aggregation_method: str,
    time_range_start: datetime,
    time_range_end: datetime,
    included_filters: Dict[str, Any],
    is_mixed_sample: bool = False,
    normalization_notes: str = "",
) -> MetricLineageRecord:
    return MetricLineageRecord(
        source_manifests=source_manifests,
        input_summaries=input_summaries,
        aggregation_method=aggregation_method,
        time_range_start=time_range_start,
        time_range_end=time_range_end,
        included_filters=included_filters,
        normalization_notes=normalization_notes,
        is_mixed_sample=is_mixed_sample,
        freshness_timestamp=datetime.now(),
    )


def attach_lineage_to_metric(
    metric: MetricValueRecord, lineage: MetricLineageRecord
) -> MetricValueRecord:
    metric.lineage = lineage
    return metric


def summarize_lineage_dependencies(lineage: MetricLineageRecord) -> str:
    manifest_count = len(lineage.source_manifests)
    return (
        f"Computed using {lineage.aggregation_method} over {manifest_count} manifests."
    )


def export_lineage_bundle(metrics: List[MetricValueRecord], output_path: str):
    data = []
    for m in metrics:
        if m.lineage:
            data.append(
                {"metric_name": m.metric_name, "lineage": m.lineage.model_dump()}
            )
    with open(output_path, "w") as f:
        # Convert datetime objects to string using default handler
        json.dump(data, f, indent=2, default=str)
