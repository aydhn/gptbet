import json
from pathlib import Path
from typing import Any, Dict, List

from .contracts import EvaluationRunManifest


def save_evaluation_manifest(manifest: EvaluationRunManifest, path: Path) -> None:
    """Saves the evaluation manifest to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        # Use model_dump_json for pydantic v2
        f.write(manifest.model_dump_json(indent=2))


def load_evaluation_manifest(path: Path) -> EvaluationRunManifest:
    """Loads an evaluation manifest from JSON."""
    with open(path, "r") as f:
        data = json.load(f)
    return EvaluationRunManifest(**data)
