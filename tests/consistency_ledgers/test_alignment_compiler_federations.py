import pytest

from sports_signal_bot.consistency_ledgers.alignment_federations import (
    aggregate_federated_alignment_outputs,
    build_alignment_compiler_federation,
    compute_alignment_federation_agreement,
    compute_federated_alignment_currentness,
    preserve_no_safe_visibility_in_alignment_federation,
    preserve_penalties_and_ceilings_in_alignment_federation,
)
from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentAgreementBand,
    AlignmentFederationFamily,
    FederatedAlignmentNodeRecord,
    FederatedAlignmentOutputStatus,
    FederationLinkStatus,
)
from sports_signal_bot.consistency_ledgers.federation_links import (
    add_alignment_federation_link,
    validate_alignment_federation_link,
)


def test_stale_member_caveats_federation():
    fed = build_alignment_compiler_federation(
        family=AlignmentFederationFamily.CONTEXT_ALIGNMENT_FEDERATION,
        member_refs=["node_1", "node_2"],
        currentness_policy="strict",
        ceiling_policy="preserve",
        agreement_policy="strict",
    )

    nodes = {
        "node_1": FederatedAlignmentNodeRecord(
            node_id="node_1",
            alignment_compiler_ref="comp_1",
            compiler_family="fam",
            supported_scope_refs=[],
            currentness_state="current",
            penalty_state="none",
            sovereignty_state="none",
            node_status="active",
            warnings=[],
        ),
        "node_2": FederatedAlignmentNodeRecord(
            node_id="node_2",
            alignment_compiler_ref="comp_2",
            compiler_family="fam",
            supported_scope_refs=[],
            currentness_state="stale",
            penalty_state="none",
            sovereignty_state="none",
            node_status="active",
            warnings=[],
        ),
    }

    link1 = add_alignment_federation_link(fed, "node_1", "node_2")
    links = {link1.link_id: link1}

    link1 = validate_alignment_federation_link(link1, nodes["node_1"], nodes["node_2"])
    assert link1.link_status == FederationLinkStatus.LINK_DEGRADED

    currentness = compute_federated_alignment_currentness(fed, nodes, links)
    assert not currentness.is_current
    assert "node_2" in currentness.stale_node_refs

    agreement = compute_alignment_federation_agreement(fed, nodes, currentness)
    assert agreement.agreement_band == AlignmentAgreementBand.WEAK_AGREEMENT

    penalties, ceilings = preserve_penalties_and_ceilings_in_alignment_federation(
        fed, nodes
    )

    decision = aggregate_federated_alignment_outputs(
        fed, currentness, agreement, penalties, ceilings
    )
    assert (
        decision.decision_output
        == FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_STALE
    )


def test_no_safe_visibility_preserved():
    fed = build_alignment_compiler_federation(
        family=AlignmentFederationFamily.CONTEXT_ALIGNMENT_FEDERATION,
        member_refs=["node_1"],
        currentness_policy="strict",
        ceiling_policy="preserve",
        agreement_policy="strict",
    )

    nodes = {
        "node_1": FederatedAlignmentNodeRecord(
            node_id="node_1",
            alignment_compiler_ref="comp_1",
            compiler_family="fam",
            supported_scope_refs=[],
            currentness_state="current",
            penalty_state="none",
            sovereignty_state="no_safe_recovery_hint",
            node_status="active",
            warnings=[],
        )
    }

    no_safe = preserve_no_safe_visibility_in_alignment_federation(fed, nodes)
    assert no_safe is True

    currentness = compute_federated_alignment_currentness(fed, nodes, {})
    agreement = compute_alignment_federation_agreement(fed, nodes, currentness)
    assert agreement.agreement_band == AlignmentAgreementBand.BOUNDED_AGREEMENT
