import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
from typing import Dict, List, Any
from sports_signal_bot.training.contracts import TrainingRunManifest, FoldManifest
from sports_signal_bot.core.logger import get_logger

logger = get_logger("TrainingManifestGenerator")

def generate_manifest(
    run_id: str,
    sport: str,
    market_type: str,
    label_name: str,
    model_name: str,
    split_strategy: str,
    total_train_rows: int,
    total_valid_rows: int,
    feature_count: int,
    feature_list_path: str,
    model_artifact_path: str,
    metrics_summary: Dict[str, float],
    fold_manifests: List[FoldManifest],
    warnings: List[str],
    seed: int,
    config_snapshot: Dict[str, Any],
    started_at_utc: str,
    output_path: str
) -> TrainingRunManifest:

    manifest = TrainingRunManifest(
        run_id=run_id,
        started_at_utc=started_at_utc,
        ended_at_utc=datetime.now(timezone.utc).isoformat(),
        sport=sport,
        market_type=market_type,
        label_name=label_name,
        model_name=model_name,
        split_strategy=split_strategy,
        total_train_rows=total_train_rows,
        total_valid_rows=total_valid_rows,
        feature_count=feature_count,
        feature_list_path=feature_list_path,
        model_artifact_path=model_artifact_path,
        metrics_summary=metrics_summary,
        fold_manifests=fold_manifests,
        warnings=warnings,
        seed=seed,
        config_snapshot=config_snapshot
    )

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    logger.info(f"Generated training manifest: {out_file}")
    return manifest
