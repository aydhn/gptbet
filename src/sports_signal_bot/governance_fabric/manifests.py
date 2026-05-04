import uuid
import datetime
from .contracts import (
    GovernanceTierCouncilRecord, ConsortiumSignalFabricRecord,
    BaselineRegistryFederationRecord, SovereignProjectionAuditExchangeRecord,
    GovernanceCouncilManifestRecord, SignalFabricManifestRecord,
    BaselineRegistryFederationManifestRecord, ProjectionAuditManifestRecord
)

class GovernanceFabricManifest(object):
    def __init__(self, council_manifest, fabric_manifest, fed_manifest, audit_manifest):
        self.council_manifest = council_manifest
        self.fabric_manifest = fabric_manifest
        self.federation_manifest = fed_manifest
        self.audit_manifest = audit_manifest

    def dict(self):
        return {
            "council_manifest": self.council_manifest.dict(),
            "fabric_manifest": self.fabric_manifest.dict(),
            "federation_manifest": self.federation_manifest.dict(),
            "audit_manifest": self.audit_manifest.dict()
        }

def generate_governance_fabric_manifest(
    council: GovernanceTierCouncilRecord,
    fabric: ConsortiumSignalFabricRecord,
    fed: BaselineRegistryFederationRecord,
    exchange: SovereignProjectionAuditExchangeRecord
):
    ts = datetime.datetime.utcnow().isoformat()
    return GovernanceFabricManifest(
        council_manifest=GovernanceCouncilManifestRecord(
            manifest_id=f"man_c_{uuid.uuid4().hex[:8]}",
            timestamp=ts,
            council_refs=[council.council_id]
        ),
        fabric_manifest=SignalFabricManifestRecord(
            manifest_id=f"man_f_{uuid.uuid4().hex[:8]}",
            timestamp=ts,
            fabric_refs=[fabric.signal_fabric_id]
        ),
        fed_manifest=BaselineRegistryFederationManifestRecord(
            manifest_id=f"man_fed_{uuid.uuid4().hex[:8]}",
            timestamp=ts,
            federation_refs=[fed.baseline_federation_id]
        ),
        audit_manifest=ProjectionAuditManifestRecord(
            manifest_id=f"man_a_{uuid.uuid4().hex[:8]}",
            timestamp=ts,
            exchange_refs=[exchange.audit_exchange_id]
        )
    )
