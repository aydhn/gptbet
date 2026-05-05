from typing import List, Optional
from .contracts import (
    AssuranceSynthesizerFederationRecord,
    FederatedAssuranceNodeRecord,
    AssuranceFederationLinkRecord,
    AssuranceFederationCurrentnessRecord,
    AssuranceFederationPenaltyRecord,
    AssuranceFederationCeilingRecord,
    AssuranceFederationAgreementRecord,
    AssuranceFederationDecisionRecord,
    FederationLinkStatus,
    FederatedAssuranceOutput,
    AssuranceFederationAgreementBand
)

def build_assurance_synthesizer_federation(federation_id: str, family: str) -> AssuranceSynthesizerFederationRecord:
    return AssuranceSynthesizerFederationRecord(
        assurance_federation_id=federation_id,
        federation_family=family,
        member_assurance_synthesizer_refs=[],
        active_link_refs=[],
        currentness_policy_ref="default_currentness_policy",
        ceiling_policy_ref="default_ceiling_policy",
        agreement_policy_ref="default_agreement_policy",
        health_status="healthy",
        warnings=[]
    )

def add_assurance_federation_link(federation: AssuranceSynthesizerFederationRecord, link: AssuranceFederationLinkRecord) -> None:
    federation.active_link_refs.append(link.link_id)

def validate_assurance_federation_link(link: AssuranceFederationLinkRecord) -> bool:
    return link.status != FederationLinkStatus.link_blocked

def compute_federated_assurance_currentness(nodes: List[FederatedAssuranceNodeRecord]) -> str:
    if any(n.currentness_state == "stale" for n in nodes):
        return "stale"
    return "current"

def summarize_assurance_federation_health(federation: AssuranceSynthesizerFederationRecord) -> str:
    if "stale_member" in federation.warnings:
        return "degraded"
    return federation.health_status

def aggregate_federated_assurance_outputs(decisions: List[AssuranceFederationDecisionRecord]) -> FederatedAssuranceOutput:
    # Stale members cap agreement quality
    if any(d.outcome == FederatedAssuranceOutput.federated_assurance_stale for d in decisions):
        return FederatedAssuranceOutput.federated_assurance_stale

    if any(d.outcome == FederatedAssuranceOutput.federated_assurance_blocked for d in decisions):
        return FederatedAssuranceOutput.federated_assurance_blocked

    if any(d.outcome == FederatedAssuranceOutput.federated_assurance_review_only for d in decisions):
        return FederatedAssuranceOutput.federated_assurance_review_only

    return FederatedAssuranceOutput.federated_assurance_current_with_caps

def preserve_penalties_and_ceilings_in_assurance_federation(federation: AssuranceSynthesizerFederationRecord, penalty: AssuranceFederationPenaltyRecord, ceiling: AssuranceFederationCeilingRecord) -> None:
    federation.warnings.append(f"Penalty preserved: {penalty.reason}")
    federation.warnings.append(f"Ceiling applied: {ceiling.cap}")

def preserve_no_safe_visibility_in_assurance_federation(federation: AssuranceSynthesizerFederationRecord) -> None:
    federation.warnings.append("no_safe_recovery_hint_preserved")

def explain_federated_assurance_output(outcome: FederatedAssuranceOutput) -> str:
    return f"Assurance output resulted in {outcome.value} due to currentness, evidence gaps or sovereignty constraints."

def compute_assurance_federation_agreement(decisions: List[AssuranceFederationDecisionRecord]) -> AssuranceFederationAgreementBand:
    if not decisions:
        return AssuranceFederationAgreementBand.no_agreement

    if any(d.outcome == FederatedAssuranceOutput.federated_assurance_blocked for d in decisions):
        return AssuranceFederationAgreementBand.no_agreement

    if any(d.outcome == FederatedAssuranceOutput.federated_assurance_stale for d in decisions):
        return AssuranceFederationAgreementBand.bounded_agreement

    return AssuranceFederationAgreementBand.strong_agreement_with_caveats

def detect_assurance_agreement_instability(agreement: AssuranceFederationAgreementBand) -> bool:
    return agreement in (AssuranceFederationAgreementBand.no_agreement, AssuranceFederationAgreementBand.weak_agreement)

def summarize_assurance_federation_agreement(agreement: AssuranceFederationAgreementBand) -> str:
    return f"Agreement band is {agreement.value}"

def explain_assurance_agreement_caps(agreement: AssuranceFederationAgreementBand) -> str:
    return "Agreement capped due to missing no-safe visibility or stale inputs."
