from .contracts import AssuranceInteroperabilityManifest
from typing import Dict, Any

def build_assurance_exchange_manifest(manifest_id: str) -> AssuranceInteroperabilityManifest:
    """Builds an interoperability manifest."""
    return AssuranceInteroperabilityManifest(
        manifest_id=manifest_id
    )

def dump_manifest_to_dict(manifest: AssuranceInteroperabilityManifest) -> Dict[str, Any]:
    return manifest.model_dump()
