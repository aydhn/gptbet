from typing import Dict, Any
from .manifests import StandardManifest
from .envelopes import ManifestEnvelopeRecord
from .registry import SchemaRegistry
from .versions import SchemaVersionRecord

class PayloadNormalizer:
    def normalize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return payload

class ManifestShim:
    def shim(self, legacy_manifest: Dict[str, Any]) -> StandardManifest:
        return StandardManifest(
            manifest_family=legacy_manifest.get("family", "unknown"),
            schema_version="0.0.0",
            producer_component="legacy_shim",
            artifact_family=legacy_manifest.get("type", "unknown"),
            artifact_id=legacy_manifest.get("id", "legacy_id"),
            run_id=legacy_manifest.get("run_id", "legacy_run_id"),
            payload=legacy_manifest.get("payload", legacy_manifest)
        )

    def detect_legacy_manifest(self, data: Dict[str, Any]) -> bool:
        return "schema_version" not in data

    def wrap_legacy_manifest(self, data: Dict[str, Any]) -> ManifestEnvelopeRecord:
        return ManifestEnvelopeRecord(
            manifest_family=data.get("family", "unknown"),
            schema_name="legacy",
            schema_version="v0.0.0",
            manifest_version="v1.0.0",
            producer_component="legacy",
            artifact_family="unknown",
            payload=data,
            warnings=["Legacy manifest wrapped"]
        )

    def infer_legacy_version(self, data: Dict[str, Any]) -> str:
        return "v0.0.0"

    def migrate_legacy_to_standard(self, data: Dict[str, Any]) -> StandardManifest:
        return self.shim(data)

class ContractAdapter:
    def adapt(self, payload: Dict[str, Any], target_version: SchemaVersionRecord) -> Dict[str, Any]:
        return payload

class VersionedLoader:
    def __init__(self, registry: SchemaRegistry, adapter: ContractAdapter):
        self.registry = registry
        self.adapter = adapter
        self.shim = ManifestShim()

    def load(self, data: Dict[str, Any], family: str) -> Dict[str, Any]:
        if self.shim.detect_legacy_manifest(data):
            wrapped = self.shim.wrap_legacy_manifest(data)
            return wrapped.dict()
        return data

class LoaderCompatibilityFacade:
    def __init__(self, loader: VersionedLoader):
        self.loader = loader

    def load_compatible(self, data: Dict[str, Any], family: str) -> Dict[str, Any]:
        return self.loader.load(data, family)
