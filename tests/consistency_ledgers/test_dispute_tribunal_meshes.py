import pytest

from sports_signal_bot.consistency_ledgers.contracts import (
    MeshPressureState,
    TribunalMeshEdgeStatus,
    TribunalMeshFamily,
    TribunalMeshRouteOutcome,
    TribunalNodeFamily,
)
from sports_signal_bot.consistency_ledgers.mesh_nodes import add_tribunal_mesh_node
from sports_signal_bot.consistency_ledgers.mesh_paths import (
    apply_tribunal_mesh_constraints,
    enumerate_tribunal_mesh_paths,
    score_tribunal_mesh_paths,
    select_tribunal_mesh_path,
)
from sports_signal_bot.consistency_ledgers.tribunal_meshes import (
    add_tribunal_mesh_edge,
    build_dispute_tribunal_mesh,
    compute_tribunal_mesh_pressure,
    validate_tribunal_mesh_edge,
)


def test_insufficient_evidence_blocks_bounded_context():
    mesh = build_dispute_tribunal_mesh(
        family=TribunalMeshFamily.BOUNDED_CONTEXT_DISPUTE_MESH,
        routing_policy="strict",
        escalation_policy="standard",
        pressure_policy="standard",
    )

    node1 = add_tribunal_mesh_node(
        mesh, TribunalNodeFamily.TRIBUNAL_INGRESS_NODE, ["t1"], ["case_fam_1"]
    )
    node2 = add_tribunal_mesh_node(
        mesh, TribunalNodeFamily.PROOF_SUFFICIENCY_NODE, ["t2"], ["case_fam_1"]
    )
    node2.backlog_state = (
        "critical"  # Simulate insufficient replay capability causing backlog
    )

    nodes = {node1.node_id: node1, node2.node_id: node2}

    edge = add_tribunal_mesh_edge(
        mesh, node1.node_id, node2.node_id, ["case_fam_1"], ["narrow"], "preserve"
    )
    edge = validate_tribunal_mesh_edge(edge, node1, node2)
    edges = {edge.edge_id: edge}

    paths = enumerate_tribunal_mesh_paths(mesh, node1.node_id, node2.node_id, edges)
    scored = score_tribunal_mesh_paths(paths, edges, nodes)

    assert scored[0]["outcome"] == TribunalMeshRouteOutcome.REVIEW_ONLY_TRIBUNAL_ROUTE

    path_record = select_tribunal_mesh_path(scored, mesh.tribunal_mesh_id)
    assert path_record.outcome == TribunalMeshRouteOutcome.REVIEW_ONLY_TRIBUNAL_ROUTE
