from sports_signal_bot.end_state_review.contracts import (
    FederationLinkStatus,
    FederatedAssuranceOutput,
    AssuranceFederationAgreementBand,
    ClosureMeshEdgeStatus,
    ClosureRouteOutcome,
    ExchangeStatus,
    AssuranceExchangeRouteOutcome,
    EndStateReviewBand,
    AssuranceFederationLinkRecord,
    FederatedAssuranceNodeRecord,
    AssuranceFederationDecisionRecord,
    ClosureMeshEdgeRecord,
    AssuranceExchangePacketRecord,
    EndStateReviewInputRecord,
    EndStateReviewPenaltyRecord
)
from sports_signal_bot.end_state_review.assurance_federations import (
    build_assurance_synthesizer_federation,
    add_assurance_federation_link,
    validate_assurance_federation_link,
    compute_federated_assurance_currentness,
    summarize_assurance_federation_health,
    aggregate_federated_assurance_outputs,
    preserve_penalties_and_ceilings_in_assurance_federation,
    preserve_no_safe_visibility_in_assurance_federation,
    explain_federated_assurance_output,
    compute_assurance_federation_agreement,
    detect_assurance_agreement_instability,
    summarize_assurance_federation_agreement,
    explain_assurance_agreement_caps
)
from sports_signal_bot.end_state_review.closure_meshes import (
    build_council_closure_mesh,
    add_closure_mesh_node,
    add_closure_mesh_edge,
    validate_closure_mesh_edge,
    summarize_closure_mesh_health,
    create_closure_checkpoint,
    verify_closure_checkpoint,
    summarize_closure_checkpoint_progress,
    detect_closure_checkpoint_regression,
    detect_closure_residue,
    record_closure_residue,
    summarize_closure_residue,
    explain_closure_residue_effect
)
from sports_signal_bot.end_state_review.assurance_exchanges import (
    build_evidence_assurance_exchange,
    validate_assurance_exchange_packet,
    route_assurance_exchange_packet,
    replay_assurance_exchange,
    summarize_assurance_exchange,
    compute_assurance_exchange_pressure,
    compute_assurance_exchange_fairness,
    preserve_fairness_without_scope_widening,
    summarize_assurance_exchange_pressure_and_fairness
)
from sports_signal_bot.end_state_review.review_compilers import (
    build_governance_end_state_review_compiler,
    register_end_state_review_input,
    execute_end_state_review_passes,
    summarize_end_state_review_compiler,
    apply_end_state_review_penalties,
    compute_end_state_review_band,
    explain_end_state_review_output,
    summarize_review_penalty_pressure
)

def test_assurance_synthesizer_federations():
    federation = build_assurance_synthesizer_federation("fed-1", "context_assurance_federation")
    assert federation.health_status == "healthy"

    link = AssuranceFederationLinkRecord(link_id="link-1", source_ref="src", target_ref="tgt", status=FederationLinkStatus.link_current)
    add_assurance_federation_link(federation, link)
    assert len(federation.active_link_refs) == 1
    assert validate_assurance_federation_link(link) is True

    nodes = [
        FederatedAssuranceNodeRecord(node_id="n1", assurance_synthesizer_ref="s1", synthesizer_family="fam", supported_scope_refs=[], currentness_state="stale", penalty_state="none", sovereignty_state="ok", node_status="active")
    ]
    assert compute_federated_assurance_currentness(nodes) == "stale"

    decisions = [AssuranceFederationDecisionRecord(decision_id="d1", outcome=FederatedAssuranceOutput.federated_assurance_stale)]
    assert aggregate_federated_assurance_outputs(decisions) == FederatedAssuranceOutput.federated_assurance_stale
    assert compute_assurance_federation_agreement(decisions) == AssuranceFederationAgreementBand.bounded_agreement

def test_council_closure_meshes():
    mesh = build_council_closure_mesh("mesh-1", "bounded_council_closure_mesh")
    assert mesh.health_status == "healthy"

    edge = ClosureMeshEdgeRecord(edge_id="e1", source_node_ref="n1", target_node_ref="n2", supported_case_families=[], supported_scope_classes=[], caveat_transfer_policy="keep", currentness_state="current", edge_status=ClosureMeshEdgeStatus.edge_current)
    add_closure_mesh_edge(mesh, edge)
    assert validate_closure_mesh_edge(edge) is True

def test_evidence_assurance_exchanges():
    exchange = build_evidence_assurance_exchange("exch-1")
    assert exchange.exchange_status == ExchangeStatus.prepared

    packet = AssuranceExchangePacketRecord(assurance_exchange_packet_id="p1", source_listing_refs=[], source_request_refs=[], source_trace_refs=[], source_evidence_refs=[], source_assurance_refs=[], evidence_completeness="partial", currentness_refs=[], caveat_refs=[], scope_constraints=[])
    validate_assurance_exchange_packet(packet)
    assert "Incomplete evidence" in packet.warnings
    assert route_assurance_exchange_packet(packet) == AssuranceExchangeRouteOutcome.routed_caveated_assurance_exchange

def test_governance_end_state_review_compilers():
    compiler = build_governance_end_state_review_compiler("comp-1", "composite_governance_end_state_review_compiler")

    input_rec = EndStateReviewInputRecord(review_input_id="in-1", input_family="trace", source_ref="s1", currentness_state="stale", caveat_state="none", sovereignty_state="ok", no_safe_visibility_state="ok")
    register_end_state_review_input(compiler, input_rec)
    assert "stale_input_registered" in compiler.warnings

    execute_end_state_review_passes(compiler)
    assert compiler.current_state == "passes_executed"

    penalty = EndStateReviewPenaltyRecord(penalty_id="pen-1", family="stale_context_penalty")
    apply_end_state_review_penalties(compiler, [penalty])
    assert len(compiler.penalty_refs) == 1

    band = compute_end_state_review_band(compiler)
    assert band == EndStateReviewBand.bounded_end_state_with_caveats
