from typing import Any, Dict, List, Optional

from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentAgreementBand,
    AlignmentCompilerFederationRecord,
    AlignmentFederationAgreementRecord,
    AlignmentFederationCeilingRecord,
    AlignmentFederationCurrentnessRecord,
    AlignmentFederationDecisionRecord,
    AlignmentFederationFamily,
    AlignmentFederationHealthRecord,
    AlignmentFederationLinkRecord,
    AlignmentFederationPenaltyRecord,
    FederatedAlignmentNodeRecord,
    FederatedAlignmentOutputStatus,
    FederationLinkStatus,
    HealthStatus,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def build_alignment_compiler_federation(
    family: AlignmentFederationFamily,
    member_refs: List[str],
    currentness_policy: str,
    ceiling_policy: str,
    agreement_policy: str,
) -> AlignmentCompilerFederationRecord:
    """Builds a new Alignment Compiler Federation."""
    return AlignmentCompilerFederationRecord(
        alignment_federation_id=generate_id("align_fed"),
        federation_family=family,
        member_alignment_compiler_refs=member_refs,
        active_link_refs=[],
        currentness_policy_ref=currentness_policy,
        ceiling_policy_ref=ceiling_policy,
        agreement_policy_ref=agreement_policy,
        health_status=HealthStatus.HEALTHY,
        warnings=[],
    )


def compute_federated_alignment_currentness(
    federation: AlignmentCompilerFederationRecord,
    nodes: Dict[str, FederatedAlignmentNodeRecord],
    links: Dict[str, AlignmentFederationLinkRecord],
) -> AlignmentFederationCurrentnessRecord:
    """Computes the currentness of the federation. Stale nodes result in false currentness."""
    stale_nodes = []

    for link_ref in federation.active_link_refs:
        if link_ref in links:
            link = links[link_ref]
            if link.target_node_ref in nodes:
                node = nodes[link.target_node_ref]
                if node.currentness_state != "current":
                    stale_nodes.append(node.node_id)
            if link.source_node_ref in nodes:
                node = nodes[link.source_node_ref]
                if (
                    node.currentness_state != "current"
                    and node.node_id not in stale_nodes
                ):
                    stale_nodes.append(node.node_id)

    is_current = len(stale_nodes) == 0

    warnings = []
    if not is_current:
        warnings.append("Federation currentness compromised due to stale member nodes.")

    return AlignmentFederationCurrentnessRecord(
        record_id=generate_id("fed_curr"),
        federation_id=federation.alignment_federation_id,
        is_current=is_current,
        stale_node_refs=stale_nodes,
        warnings=warnings,
    )


def compute_alignment_federation_agreement(
    federation: AlignmentCompilerFederationRecord,
    nodes: Dict[str, FederatedAlignmentNodeRecord],
    currentness: AlignmentFederationCurrentnessRecord,
) -> AlignmentFederationAgreementRecord:
    """Computes agreement band, capping quality if there is staleness or no_safe visibility failures."""

    warnings = []
    band = AlignmentAgreementBand.STABLE_AGREEMENT

    if not currentness.is_current:
        band = AlignmentAgreementBand.WEAK_AGREEMENT
        warnings.append("Stale member output caps agreement quality to WEAK_AGREEMENT.")

    for node_id in federation.member_alignment_compiler_refs:
        if node_id in nodes:
            node = nodes[node_id]
            if (
                "no_safe_recovery_hint" in node.sovereignty_state
                or "no_safe_visibility_failure" in getattr(node, "warnings", [])
            ):
                band = AlignmentAgreementBand.BOUNDED_AGREEMENT
                warnings.append("No-safe visibility failure limits stable agreement.")
                break

    return AlignmentFederationAgreementRecord(
        record_id=generate_id("fed_agr"),
        federation_id=federation.alignment_federation_id,
        agreement_band=band,
        warnings=warnings,
    )


def preserve_penalties_and_ceilings_in_alignment_federation(
    federation: AlignmentCompilerFederationRecord,
    nodes: Dict[str, FederatedAlignmentNodeRecord],
) -> tuple[AlignmentFederationPenaltyRecord, AlignmentFederationCeilingRecord]:

    penalties = []
    ceilings = []

    for node_id in federation.member_alignment_compiler_refs:
        if node_id in nodes:
            node = nodes[node_id]
            if node.penalty_state != "none":
                penalties.append(f"Penalty from {node.node_id}: {node.penalty_state}")
            if "ceiling" in node.sovereignty_state.lower():
                ceilings.append(
                    f"Ceiling from {node.node_id}: {node.sovereignty_state}"
                )

    return (
        AlignmentFederationPenaltyRecord(
            record_id=generate_id("fed_pen"),
            federation_id=federation.alignment_federation_id,
            penalties=penalties,
            warnings=["Penalties preserved from members."] if penalties else [],
        ),
        AlignmentFederationCeilingRecord(
            record_id=generate_id("fed_ceil"),
            federation_id=federation.alignment_federation_id,
            ceilings=ceilings,
            warnings=["Ceilings preserved from members."] if ceilings else [],
        ),
    )


def aggregate_federated_alignment_outputs(
    federation: AlignmentCompilerFederationRecord,
    currentness: AlignmentFederationCurrentnessRecord,
    agreement: AlignmentFederationAgreementRecord,
    penalties: AlignmentFederationPenaltyRecord,
    ceilings: AlignmentFederationCeilingRecord,
) -> AlignmentFederationDecisionRecord:
    """Aggregates the state to a final bounded output."""

    output_status = FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_CURRENT_WITH_CAPS
    warnings = []

    if not currentness.is_current:
        output_status = FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_STALE
        warnings.append("Stale inputs lead to STALE output.")
    elif agreement.agreement_band in [
        AlignmentAgreementBand.WEAK_AGREEMENT,
        AlignmentAgreementBand.NO_AGREEMENT,
    ]:
        output_status = FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_DEGRADED
        warnings.append("Weak or no agreement leads to DEGRADED output.")
    elif penalties.penalties or ceilings.ceilings:
        output_status = FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_CAVEATED
        warnings.append("Preserved penalties/ceilings lead to CAVEATED output.")

    return AlignmentFederationDecisionRecord(
        record_id=generate_id("fed_dec"),
        federation_id=federation.alignment_federation_id,
        decision_output=output_status,
        warnings=warnings,
    )


def preserve_no_safe_visibility_in_alignment_federation(
    federation: AlignmentCompilerFederationRecord,
    nodes: Dict[str, FederatedAlignmentNodeRecord],
) -> bool:
    """Checks if any node has a no_safe_recovery_hint."""
    for node_id in federation.member_alignment_compiler_refs:
        if node_id in nodes:
            node = nodes[node_id]
            if "no_safe_recovery_hint" in node.sovereignty_state or any(
                "no_safe_recovery_hint" in w for w in node.warnings
            ):
                return True
    return False


def explain_federated_alignment_output(
    decision: AlignmentFederationDecisionRecord,
    currentness: AlignmentFederationCurrentnessRecord,
    agreement: AlignmentFederationAgreementRecord,
    penalties: AlignmentFederationPenaltyRecord,
    ceilings: AlignmentFederationCeilingRecord,
    no_safe_preserved: bool,
) -> Dict[str, Any]:
    """Generates an explanation of the federated alignment output."""
    return {
        "decision": decision.decision_output.value,
        "is_current": currentness.is_current,
        "agreement_band": agreement.agreement_band.value,
        "penalties": penalties.penalties,
        "ceilings": ceilings.ceilings,
        "no_safe_visibility_preserved": no_safe_preserved,
        "warnings": decision.warnings + currentness.warnings + agreement.warnings,
    }
