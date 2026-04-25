import json
from typing import Any, Dict, List

import pandas as pd

from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 PeriodRegimeRecord,
                                                 RegimeManifest)


def export_event_regimes_csv(records: List[EventRegimeRecord], path: str):
    data = [r.model_dump(exclude={"supporting_features", "warnings"}) for r in records]
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def export_period_regimes_csv(records: List[PeriodRegimeRecord], path: str):
    data = [
        r.model_dump(exclude={"derived_from_window", "supporting_metrics", "warnings"})
        for r in records
    ]
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def export_regime_manifest(manifest: RegimeManifest, path: str):
    with open(path, "w") as f:
        json.dump(manifest.model_dump(mode="json"), f, indent=2)


def generate_regime_summary(manifest: RegimeManifest) -> str:
    lines = ["--- Regime Summary ---"]
    for family in manifest.active_families:
        lines.append(f"Family: {family}")
        for cov in manifest.coverage_summaries:
            if cov.regime_family == family:
                lines.append(
                    f"  - {cov.regime_label}: {cov.row_count} events ({cov.coverage_rate:.2%})"
                )
                if not cov.minimum_rows_satisfied:
                    lines.append("    [WARNING: Low sample size]")
    return "\n".join(lines)
