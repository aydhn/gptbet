import uuid
import json
from datetime import datetime
from typing import List
from .contracts import PolicyManifest

def generate_manifest(active_bundles: List[str], active_overlays: List[str], pending_changes: int, recent_conflicts: int) -> PolicyManifest:
    return PolicyManifest(
        manifest_id=f"pm_{uuid.uuid4().hex[:8]}",
        active_bundles=active_bundles,
        active_overlays=active_overlays,
        pending_changes=pending_changes,
        recent_conflicts=recent_conflicts
    )

def dump_manifest(manifest: PolicyManifest, filepath: str = "policy_as_code_manifest.json"):
    with open(filepath, "w") as f:
         f.write(manifest.model_dump_json(indent=2))
