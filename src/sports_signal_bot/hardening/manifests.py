"""
Manifest generation logic.
"""
from .contracts import HardeningManifestRecord
import json
from dataclasses import asdict

def serialize_manifest(manifest: HardeningManifestRecord) -> str:
    return json.dumps(asdict(manifest), indent=2, sort_keys=True)
