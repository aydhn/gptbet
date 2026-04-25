from typing import Dict, List

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeCoverageRecord)
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def calculate_coverage(
    records: List[EventRegimeRecord], config: RegimeThresholdsConfig
) -> List[RegimeCoverageRecord]:
    family_label_counts: Dict[str, Dict[str, int]] = {}
    total_events = len(set(r.event_id for r in records))

    if total_events == 0:
        return []

    for record in records:
        family = record.regime_family
        label = record.regime_label

        if family not in family_label_counts:
            family_label_counts[family] = {}
        if label not in family_label_counts[family]:
            family_label_counts[family][label] = 0

        family_label_counts[family][label] += 1

    coverage_records = []

    for family, labels in family_label_counts.items():
        for label, count in labels.items():
            rate = count / total_events
            min_satisfied = count >= config.minimum_rows_per_regime
            warnings = []
            if not min_satisfied:
                warnings.append(
                    f"Low sample size: {count} < {config.minimum_rows_per_regime}"
                )

            coverage_records.append(
                RegimeCoverageRecord(
                    regime_family=family,
                    regime_label=label,
                    row_count=count,
                    coverage_rate=rate,
                    minimum_rows_satisfied=min_satisfied,
                    warnings=warnings,
                )
            )

    return coverage_records
