import json
from pathlib import Path

from sports_signal_bot.ratings.contracts import RatingBuildManifest


def write_rating_manifest(manifest: RatingBuildManifest, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"rating_manifest_{manifest.run_id}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest.model_dump(mode="json"), f, indent=2)
    return manifest_path
