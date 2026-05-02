import uuid
from sports_signal_bot.ecosystem_discovery.contracts import (
    EcosystemDiscoveryManifest,
    DiscoveryCoverageRecord,
    EcosystemDirectoryRecord
)

def compute_ecosystem_discovery_coverage(directory: EcosystemDirectoryRecord) -> DiscoveryCoverageRecord:
    rec = DiscoveryCoverageRecord()
    if len(directory.registries) > 0:
        rec.registry_coverage = "usable"
    if len(directory.verifier_nodes) > 0:
        rec.verifier_profile_coverage = "usable"
    if len(directory.catalogs) > 0:
        rec.spec_bundle_coverage = "usable"
    return rec

def build_ecosystem_manifest(directory: EcosystemDirectoryRecord) -> EcosystemDiscoveryManifest:
    return EcosystemDiscoveryManifest(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        directory_ref=directory.directory_id,
        catalogs=[c.node_id for c in directory.catalogs],
        coverage=compute_ecosystem_discovery_coverage(directory)
    )
