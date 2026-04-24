import json
from typing import Dict, Any, List
from pathlib import Path

from sports_signal_bot.calibration.contracts import CalibrationRunManifest

def save_calibration_manifest(manifest: CalibrationRunManifest, output_path: str) -> None:
    """Saves the CalibrationRunManifest to a JSON file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(manifest.model_dump_json(indent=2))
