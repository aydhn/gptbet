import json
from .contracts import ComplianceManifest

def save_manifest(manifest: ComplianceManifest, path: str):
    with open(path, 'w') as f:
        f.write(manifest.model_dump_json(indent=2))

def load_manifest(path: str) -> ComplianceManifest:
    with open(path, 'r') as f:
        data = json.load(f)
        return ComplianceManifest(**data)
