import uuid
from typing import List
from src.sports_signal_bot.planetary_hardening.contracts import (
    GlobalQuorumFederationRecord,
    FederatedQuorumNodeRecord,
    QuorumFederationLinkRecord,
    QuorumFederationAgreementRecord,
    GlobalQuorumFederationWarningRecord
)

def build_global_quorum_federation(family: str, nodes: List[FederatedQuorumNodeRecord]) -> GlobalQuorumFederationRecord:
    return GlobalQuorumFederationRecord(
        global_quorum_federation_id=f"gqf_{uuid.uuid4().hex[:8]}",
        federation_family=family,
        member_quorum_refs=nodes,
        federation_status="federation_review_only"
    )

def add_quorum_federation_link(federation: GlobalQuorumFederationRecord, link: QuorumFederationLinkRecord) -> GlobalQuorumFederationRecord:
    federation.active_link_refs.append(link)
    return federation

def verify_global_quorum_federation(federation: GlobalQuorumFederationRecord, cap_on_stale: bool = True) -> GlobalQuorumFederationRecord:
    warnings = []
    has_stale = any(n.is_stale for n in federation.member_quorum_refs)

    if has_stale:
        warnings.append(GlobalQuorumFederationWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Stale member in federation."))
        if cap_on_stale:
            federation.federation_status = "federation_caveated"

    if not federation.member_quorum_refs:
        warnings.append(GlobalQuorumFederationWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Empty federation."))
        federation.federation_status = "federation_gapped"

    if not warnings and federation.member_quorum_refs:
        federation.federation_status = "federation_verified" # Non-authoritative, but verified integrity

    federation.warnings.extend(warnings)
    return federation

def compute_quorum_federation_agreement(federation: GlobalQuorumFederationRecord) -> GlobalQuorumFederationRecord:
    has_stale = any(n.is_stale for n in federation.member_quorum_refs)
    band = "bounded_agreement" if has_stale else "stable_agreement"

    # Even if stable, it's non-authoritative.
    federation.agreement_refs.append(QuorumFederationAgreementRecord(
        agreement_id=f"agr_{uuid.uuid4().hex[:8]}",
        agreement_band=band
    ))
    return federation

def summarize_global_quorum_federation(federation: GlobalQuorumFederationRecord) -> dict:
    return {
        "id": federation.global_quorum_federation_id,
        "family": federation.federation_family,
        "status": federation.federation_status,
        "warnings": [w.message for w in federation.warnings],
        "members_count": len(federation.member_quorum_refs)
    }
