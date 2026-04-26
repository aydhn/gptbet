import json
from pathlib import Path

from sports_signal_bot.dynamic_weighting.contracts import WeightingManifest


def save_weighting_manifest(manifest: WeightingManifest, output_dir: str):
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / f"weighting_manifest_{manifest.run_id}.json"
    with open(file_path, "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    return file_path
