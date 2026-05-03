import datetime
import uuid
import json
from typing import List
from sports_signal_bot.distributed_coordination.contracts import DistributedFabricManifest

class DistributedManifestManager:
    """Manages the creation and export of distributed fabric manifests."""

    def build_fabric_manifest(self, cluster_refs: List[str]) -> DistributedFabricManifest:
        """Builds the root distributed fabric manifest."""
        return DistributedFabricManifest(
            manifest_id=f"manifest_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            cluster_refs=cluster_refs
        )

    def export_manifest(self, manifest: DistributedFabricManifest, path: str) -> None:
        """Exports the manifest to a JSON file."""
        data = {
            "manifest_id": manifest.manifest_id,
            "timestamp": manifest.timestamp.isoformat(),
            "cluster_refs": manifest.cluster_refs
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
