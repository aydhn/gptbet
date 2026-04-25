import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.features.contracts import FeatureAvailabilitySummary

logger = get_logger("FeatureAvailabilityGenerator")


def generate_availability_summary(
    run_id: str,
    builder_outputs: Dict[str, pd.DataFrame],
    missing_sources: List[str],
    skipped_builders: List[str],
    output_path: str,
) -> FeatureAvailabilitySummary:

    counts = {
        name: len(df.columns) - 1 for name, df in builder_outputs.items()
    }  # -1 for event_id

    summary = FeatureAvailabilitySummary(
        run_id=run_id,
        builder_column_counts=counts,
        missing_sources=missing_sources,
        skipped_builders=skipped_builders,
    )

    out_file = Path(output_path).with_name(
        f"{Path(output_path).stem}_availability.json"
    )
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        f.write(summary.model_dump_json(indent=2))

    logger.info(f"Generated feature availability summary: {out_file}")
    return summary
