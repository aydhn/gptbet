from typing import List, Dict, Any
from .contracts import (
    ObservatoryFederationRecord,
    ObservatoryFederationFamily,
    ObservatoryFederationStatus,
    FederatedObservatoryNodeRecord,
    ObservatoryFederationLinkRecord,
    ObservatoryFederationAgreementRecord,
    ObservatoryFederationHealthRecord
)

def build_observatory_federation(fed_id: str, family: ObservatoryFederationFamily) -> ObservatoryFederationRecord:
    return ObservatoryFederationRecord(
        observatory_federation_id=fed_id,
        federation_family=family,
        federation_status=ObservatoryFederationStatus.federation_gapped
    )

def add_observatory_federation_link(fed: ObservatoryFederationRecord, link: ObservatoryFederationLinkRecord) -> ObservatoryFederationRecord:
    fed.active_link_refs.append(link.link_id)
    return fed

def verify_observatory_federation(fed: ObservatoryFederationRecord, nodes: List[FederatedObservatoryNodeRecord]) -> ObservatoryFederationRecord:
    has_stale = any(n.is_stale for n in nodes)
    has_caveats = len(fed.warnings) > 0

    if has_stale:
        fed.federation_status = ObservatoryFederationStatus.federation_review_only
    elif has_caveats:
        fed.federation_status = ObservatoryFederationStatus.federation_caveated
    else:
        fed.federation_status = ObservatoryFederationStatus.federation_verified

    if not nodes:
        fed.federation_status = ObservatoryFederationStatus.federation_gapped

    return fed

def compute_observatory_federation_agreement(fed: ObservatoryFederationRecord) -> ObservatoryFederationAgreementRecord:
    return ObservatoryFederationAgreementRecord(
        agreement_id=f"agree_{fed.observatory_federation_id}",
        agreed_on="current_utc"
    )

def summarize_observatory_federation(fed: ObservatoryFederationRecord) -> Dict[str, Any]:
    return {
        "id": fed.observatory_federation_id,
        "status": fed.federation_status,
        "links": len(fed.active_link_refs),
        "residues": len(fed.residue_refs),
        "caveats": len(fed.warnings)
    }
