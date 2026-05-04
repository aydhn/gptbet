from typing import List
from sports_signal_bot.federation_ecosystem.contracts import (
    AttestationExchangeHubRecord, HubAdmissionRecord, HubRoutingDecisionRecord
)

def build_attestation_hub(hub_id: str, family: str) -> AttestationExchangeHubRecord:
    return AttestationExchangeHubRecord(
        hub_id=hub_id,
        hub_family=family,
        supported_attestation_families=[],
        supported_exchange_scopes=[],
        participant_refs=[],
        queue_refs=[],
        routing_policy_ref="default",
        health_status="healthy",
        warnings=[]
    )

def evaluate_hub_admission(packet_ref: str, source_ref: str, validity_state: str, caveat_state: str) -> HubAdmissionRecord:
    status = "blocked_invalid"
    if validity_state == "valid":
        if caveat_state == "heavy":
            status = "admitted_caveated"
        else:
            status = "admitted_bounded_exchange"
    elif validity_state == "expired":
        status = "blocked_expired"

    return HubAdmissionRecord(
        admission_id=f"adm_{packet_ref}",
        incoming_packet_ref=packet_ref,
        source_registry_ref=source_ref,
        target_registry_refs=[],
        requested_scope="bounded",
        caveat_state=caveat_state,
        validity_state=validity_state,
        admission_status=status,
        warnings=[]
    )

def route_packet_through_hub(admission: HubAdmissionRecord) -> HubRoutingDecisionRecord:
    if admission.admission_status == "blocked_expired" or admission.admission_status == "blocked_invalid":
        outcome = "block_and_quarantine"
    elif admission.admission_status == "admitted_caveated":
        outcome = "route_caveated_visibility"
    elif admission.admission_status == "admitted_bounded_exchange":
        outcome = "route_bounded_exchange"
    else:
        outcome = "route_review_only"

    return HubRoutingDecisionRecord(
        decision_id=f"dec_{admission.admission_id}",
        admission_ref=admission.admission_id,
        routing_outcome=outcome,
        applied_caveats=[],
        explanation=f"Routed based on admission status: {admission.admission_status}"
    )

def propagate_exchange_caveats(decision: HubRoutingDecisionRecord, new_caveat: str) -> HubRoutingDecisionRecord:
    decision.applied_caveats.append(new_caveat)
    return decision

def summarize_hub_activity(hub: AttestationExchangeHubRecord) -> str:
    return hub.health_status
