from typing import Dict, List, Any
from datetime import datetime
from .contracts import (
    PublicationIndexRecord,
    GatewayIndexEntryRecord,
    PublicPacketRecord,
    PublicationProfileRecord,
    VerificationGatewayRecord,
    GatewayChannelRecord,
    GatewayEndpointRecord
)

def build_publication_index(
    index_id: str,
    packets: List[PublicPacketRecord]
) -> PublicationIndexRecord:
    entries = []
    for p in packets:
        # We extract profile and family from metadata
        profile = p.metadata.get("profile", "unknown")
        family = p.metadata.get("family", "unknown")

        entries.append(GatewayIndexEntryRecord(
            bundle_id=p.bundle_id,
            family=family,
            version="1.0", # Simplified versioning
            publication_profile=profile,
            proof_coverage_summary=f"{len(p.proof_refs)} proofs attached",
            notarization_summary="Notarized" if len(p.proof_refs) > 0 else "Pending",
            freshness="Current" if not p.supersession_marker else "Superseded",
            supersession_status=p.supersession_marker or "active",
            challenge_intake_endpoint_ref="/api/gateway/intake" if p.challenge_instructions else None,
            signed_checkpoint_refs=p.proof_refs
        ))

    return PublicationIndexRecord(
        index_id=index_id,
        generated_at=datetime.utcnow(),
        entries=entries
    )

def render_gateway_packet(packet: PublicPacketRecord) -> Dict[str, Any]:
    # Returns a safe dict representation for a hypothetical API response
    return {
        "packet_id": packet.packet_id,
        "bundle_id": packet.bundle_id,
        "content": packet.claimed_content,
        "proofs": packet.proof_refs,
        "redaction_notice": packet.redaction_notice,
        "caveats": packet.caveats,
        "published_at": packet.publication_time.isoformat(),
        "status": packet.supersession_marker or "active",
        "challenge_instructions": packet.challenge_instructions
    }

def validate_gateway_profile_access(profile: PublicationProfileRecord, audience: str) -> bool:
    # A simple RBAC checking if the audience string matches the profile's audience_family
    # In a real system, you'd check tokens/JWTs
    if profile.audience_family == "public" and audience in ["public", "verifier", "auditor", "partner", "internal"]:
        return True
    if profile.audience_family == "auditor" and audience in ["auditor", "partner", "internal"]:
        return True
    if profile.audience_family == "partner" and audience in ["partner", "internal"]:
        return True
    if profile.audience_family == "reviewer" and audience in ["reviewer", "internal"]:
        return True
    if profile.audience_family == "internal" and audience == "internal":
        return True
    return False

def summarize_gateway_state(gateway: VerificationGatewayRecord, index: PublicationIndexRecord) -> Dict[str, Any]:
    active_channels = [c.profile for c in gateway.channels if c.active]
    return {
        "gateway_id": gateway.gateway_id,
        "active_profiles": active_channels,
        "endpoints_count": len(gateway.endpoints),
        "total_published_entries": len(index.entries),
        "active_entries": len([e for e in index.entries if e.supersession_status == "active"]),
        "superseded_entries": len([e for e in index.entries if e.supersession_status != "active"]),
        "last_updated": index.generated_at.isoformat()
    }
