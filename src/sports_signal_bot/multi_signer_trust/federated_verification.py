from datetime import datetime
from typing import List, Tuple
from .contracts import (
    MeshVerificationRequestRecord,
    MeshVerificationResponseRecord,
    FederatedVerificationRecord,
    FederatedImportDecisionRecord,
    ImportLane
)

def build_mesh_verification_request(
    bundle_ref: str,
    source_node: str
) -> MeshVerificationRequestRecord:
    return MeshVerificationRequestRecord(
        request_id=f"mesh_req_{datetime.utcnow().timestamp()}",
        target_bundle_ref=bundle_ref,
        source_node=source_node,
        requested_at=datetime.utcnow()
    )

def collect_federated_verification_responses(
    request: MeshVerificationRequestRecord
) -> List[MeshVerificationResponseRecord]:
    # Placeholder for collecting responses from other nodes
    return []

def aggregate_mesh_verification(
    request: MeshVerificationRequestRecord,
    responses: List[MeshVerificationResponseRecord],
    local_verified: bool
) -> FederatedVerificationRecord:

    # Determine basic lane
    lane = ImportLane.REVIEW_QUARANTINE
    if local_verified and any(r.is_verified for r in responses):
        lane = ImportLane.FEDERATED_VERIFIED
    elif local_verified:
        lane = ImportLane.LOCAL_VERIFIED
    elif any(r.is_verified for r in responses):
        lane = ImportLane.TRUST_PENDING

    return FederatedVerificationRecord(
        verification_id=f"fed_ver_{datetime.utcnow().timestamp()}",
        bundle_ref=request.target_bundle_ref,
        local_verified=local_verified,
        remote_responses=responses,
        final_lane=lane
    )

def decide_federated_import_acceptance(
    verification: FederatedVerificationRecord,
    requires_federated: bool = False
) -> FederatedImportDecisionRecord:
    accepted = False
    reason = "Initial"
    lane = verification.final_lane

    if lane == ImportLane.FEDERATED_VERIFIED:
        accepted = True
        reason = "Federated and local verification successful"
    elif lane == ImportLane.LOCAL_VERIFIED:
        if requires_federated:
            accepted = False
            reason = "Requires federated countersign"
            lane = ImportLane.TRUST_PENDING
        else:
            accepted = True
            reason = "Local verification sufficient"
    else:
        accepted = False
        reason = "Insufficient verification"

    return FederatedImportDecisionRecord(
        decision_id=f"fed_dec_{datetime.utcnow().timestamp()}",
        verification_ref=verification.verification_id,
        accepted=accepted,
        lane_assigned=lane,
        reason=reason
    )

def summarize_mesh_verification(verification: FederatedVerificationRecord) -> str:
    remote_count = len(verification.remote_responses)
    remote_verified = sum(1 for r in verification.remote_responses if r.is_verified)
    return f"Local: {verification.local_verified}, Remote: {remote_verified}/{remote_count} verified. Lane: {verification.final_lane.value}"
