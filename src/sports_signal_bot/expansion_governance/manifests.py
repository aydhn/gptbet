import json
from pathlib import Path
from .contracts import ExpansionGovernanceManifest

def write_governance_manifest(manifest: ExpansionGovernanceManifest, output_dir: str = "artifacts/") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = f"{output_dir}/expansion_governance_manifest_{manifest.manifest_id}.json"
    with open(file_path, 'w') as f:
        json.dump(manifest.model_dump(mode='json'), f, indent=2)
    return file_path
