import json
import os
from pathlib import Path
from typing import Any, Dict

from sports_signal_bot.core.paths import get_processed_dir
from sports_signal_bot.research.contracts import (ResearchRunManifest,
                                                  TimeSliceSummaryRecord)


class ResearchArtifactManager:
    """Manages saving research artifacts."""

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.base_dir = get_processed_dir() / "research" / run_id
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_manifest(self, manifest: ResearchRunManifest) -> str:
        path = self.base_dir / "research_manifest.json"
        with open(path, "w") as f:
            f.write(manifest.model_dump_json(indent=2))
        return str(path)

    def save_time_slice_summary(self, summary: TimeSliceSummaryRecord) -> str:
        path = self.base_dir / "time_slice_summary.json"
        with open(path, "w") as f:
            f.write(summary.model_dump_json(indent=2))
        return str(path)

    def save_period_artifact(
        self, period_id: int, artifact_name: str, data: Dict[str, Any]
    ) -> str:
        period_dir = self.base_dir / f"period_{period_id}"
        period_dir.mkdir(exist_ok=True)
        path = period_dir / f"{artifact_name}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return str(path)
