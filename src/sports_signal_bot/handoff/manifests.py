import uuid
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from .contracts import HandoffManifest, HandoffPackageRecord, HandoffSummaryRecord

def build_handoff_manifest(
    packages: List[HandoffPackageRecord],
    summary: HandoffSummaryRecord
) -> HandoffManifest:
    return HandoffManifest(
        manifest_id=str(uuid.uuid4()),
        packages=packages,
        summary=summary,
        created_at=datetime.now(timezone.utc)
    )

def export_manifest(manifest: HandoffManifest, path: str = "handoff_manifest.json") -> str:
    with open(path, "w") as f:
        # Pydantic v2 compatible
        f.write(manifest.model_dump_json(indent=2))
    return path
