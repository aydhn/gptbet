import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
from typing import Dict, List, Any
from sports_signal_bot.features.contracts import FeatureBuildContext, FeatureManifestRecord
from sports_signal_bot.core.logger import get_logger

logger = get_logger("FeatureManifestGenerator")

def generate_manifest(
    context: FeatureBuildContext,
    data: Dict[str, pd.DataFrame],
    feature_matrix: pd.DataFrame,
    active_builders: List[Any],
    output_path: str,
    warnings: List[str] = None
) -> FeatureManifestRecord:

    if warnings is None:
        warnings = []

    source_counts = {k: len(v) for k, v in data.items()}
    null_summary = feature_matrix.isnull().sum().to_dict()

    manifest = FeatureManifestRecord(
        run_id=context.run_id,
        built_at_utc=datetime.now(timezone.utc).isoformat(),
        sport=context.sport,
        market_type=context.market_type,
        source_datasets=list(data.keys()),
        source_record_counts=source_counts,
        selected_builders=[b.name for b in active_builders],
        produced_columns=list(feature_matrix.columns),
        null_summary=null_summary,
        row_count=len(feature_matrix),
        output_path=output_path,
        warnings=warnings
    )

    # Optional: write to disk
    out_file = Path(output_path).with_suffix(".manifest.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    logger.info(f"Generated feature manifest: {out_file}")
    return manifest
