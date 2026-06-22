from typing import Any, Dict, List, Tuple

from sports_signal_bot.consistency_ledgers.alignment_federations import (
    aggregate_federated_alignment_outputs,
    compute_alignment_federation_agreement,
    compute_federated_alignment_currentness,
    preserve_no_safe_visibility_in_alignment_federation,
    preserve_penalties_and_ceilings_in_alignment_federation)
from sports_signal_bot.consistency_ledgers.clearing_routes import (
    apply_clearing_constraints, enumerate_clearing_matches,
    score_clearing_matches, select_clearing_outcome)
from sports_signal_bot.consistency_ledgers.contracts import (
    AlignmentCompilerFederationRecord, AlignmentFederationLinkRecord,
    ClearingBookRecord, ClearingListingRecord, ClearingRequestRecord,
    ConsistencyEntryParams, ConsistencyState, DisputeTribunalMeshRecord,
    EvidenceExchangeClearerRecord, FederatedAlignmentNodeRecord,
    FederatedAlignmentOutputStatus, LedgerEntryFamily,
    SovereignGovernanceConsistencyLedgerRecord, TribunalMeshEdgeRecord,
    TribunalMeshNodeRecord)
from sports_signal_bot.consistency_ledgers.evidence_clearers import \
    compute_clearing_pressure
from sports_signal_bot.consistency_ledgers.ledger_entries import \
    register_consistency_entry
from sports_signal_bot.consistency_ledgers.mesh_paths import (
    apply_tribunal_mesh_constraints, enumerate_tribunal_mesh_paths,
    score_tribunal_mesh_paths, select_tribunal_mesh_path)
from sports_signal_bot.consistency_ledgers.tribunal_meshes import \
    compute_tribunal_mesh_pressure


def build_alignment_ledger_pipeline(
    federation: AlignmentCompilerFederationRecord,
    nodes: Dict[str, FederatedAlignmentNodeRecord],
    links: Dict[str, AlignmentFederationLinkRecord],
    ledger: SovereignGovernanceConsistencyLedgerRecord,
) -> Tuple[Any, List[Any]]:
    currentness = compute_federated_alignment_currentness(
        federation, nodes, links
    )
    agreement = compute_alignment_federation_agreement(
        federation, nodes, currentness
    )
    penalties, ceilings = (
        preserve_penalties_and_ceilings_in_alignment_federation(
            federation, nodes
        )
    )

    decision = aggregate_federated_alignment_outputs(
        federation, currentness, agreement, penalties, ceilings
    )
    no_safe = preserve_no_safe_visibility_in_alignment_federation(
        federation, nodes
    )

    # Map decision to ledger consistency state
    cons_state = ConsistencyState.CONSISTENT_WITH_CAPS
    if (
        decision.decision_output
        == FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_STALE
    ):
        cons_state = ConsistencyState.STALE_CONSISTENCY
    elif (
        decision.decision_output
        == FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_DEGRADED
    ):
        cons_state = ConsistencyState.DEGRADED_CONSISTENCY
    elif (
        decision.decision_output
        == FederatedAlignmentOutputStatus.FEDERATED_ALIGNMENT_CAVEATED
    ):
        cons_state = ConsistencyState.CAVEATED_CONSISTENCY

    caveats = "no_safe_recovery_hint_preserved" if no_safe else "none"

    params = ConsistencyEntryParams(
        family=LedgerEntryFamily.CONTEXT_CONSISTENCY_ENTRY,
        source_ref=federation.alignment_federation_id,
        source_family=federation.federation_family.value,
        currentness="current" if currentness.is_current else "stale",
        consistency=cons_state,
        caveats=caveats,
    )
    entry = register_consistency_entry(ledger, params)

    return decision, [entry]


def build_tribunal_mesh_context_pipeline(
    mesh: DisputeTribunalMeshRecord,
    start_node: str,
    target_node: str,
    nodes: Dict[str, TribunalMeshNodeRecord],
    edges: Dict[str, TribunalMeshEdgeRecord],
) -> Any:
    pressure = compute_tribunal_mesh_pressure(mesh, nodes, edges)
    paths = enumerate_tribunal_mesh_paths(mesh, start_node, target_node, edges)
    scored = score_tribunal_mesh_paths(paths, edges, nodes)
    constrained = apply_tribunal_mesh_constraints(
        scored, pressure.pressure_state
    )
    return select_tribunal_mesh_path(constrained, mesh.tribunal_mesh_id)


def build_clearer_consistency_pipeline(
    clearer: EvidenceExchangeClearerRecord,
    books: Dict[str, ClearingBookRecord],
    listings: Dict[str, ClearingListingRecord],
    requests: Dict[str, ClearingRequestRecord],
) -> List[Any]:
    pressure = compute_clearing_pressure(clearer, books, listings, requests)
    outcomes = []

    for book_id in clearer.clearing_book_refs:
        if book_id in books:
            book = books[book_id]
            matches = enumerate_clearing_matches(book, listings, requests)
            scored = score_clearing_matches(matches)
            constrained = apply_clearing_constraints(
                scored, "high" if pressure.pressure_score > 50 else "low"
            )
            outcome = select_clearing_outcome(constrained)
            outcomes.append(outcome)

    return outcomes
