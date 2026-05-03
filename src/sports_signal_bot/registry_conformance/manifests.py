# manifests.py
from datetime import datetime, timezone
import uuid
import json
from .contracts import CorridorRegistryManifestRecord


def generate_registry_manifest(
    registry_ref: str, total_entries: int, current_pointers_count: int
) -> CorridorRegistryManifestRecord:
    return CorridorRegistryManifestRecord(
        manifest_id=f"manifest_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.now(timezone.utc),
        registry_ref=registry_ref,
        total_entries=total_entries,
        current_pointers_count=current_pointers_count,
    )
