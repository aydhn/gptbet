import json
from pathlib import Path
from typing import Dict, Any
from .contracts import FederatedManifest

def write_federated_manifest(manifest: FederatedManifest, output_dir: str = "artifacts/governance") -> str:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    filepath = path / f"federated_manifest_{manifest.manifest_id}.json"

    with open(filepath, 'w') as f:
        f.write(manifest.model_dump_json(indent=2))

    return str(filepath)
