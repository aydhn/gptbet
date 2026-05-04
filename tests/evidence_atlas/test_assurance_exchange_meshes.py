import pytest
from sports_signal_bot.evidence_atlas.contracts import (
    AssuranceMeshEdgeRecord,
    AssuranceMeshEdgeStatus,
    AssuranceMeshPressureState,
    AssuranceMeshPressureRecord,
    AssuranceMeshPathRecord,
    AssuranceMeshPathOutcome
)
from sports_signal_bot.evidence_atlas.assurance_meshes import (
    build_assurance_exchange_mesh,
    validate_assurance_mesh_edge,
    compute_assurance_mesh_pressure,
    downgrade_assurance_paths_due_to_pressure
)

def test_build_mesh():
    mesh = build_assurance_exchange_mesh("m1", "bounded_assurance_mesh")
    assert mesh.assurance_mesh_id == "m1"
    assert mesh.mesh_family == "bounded_assurance_mesh"

def test_validate_edge():
    good_edge = AssuranceMeshEdgeRecord(
        edge_id="e1", source_node_ref="n1", target_node_ref="n2", caveat_transfer_policy="keep",
        currentness_state="current", edge_status=AssuranceMeshEdgeStatus.edge_current
    )
    bad_edge = AssuranceMeshEdgeRecord(
        edge_id="e2", source_node_ref="n1", target_node_ref="n2", caveat_transfer_policy="keep",
        currentness_state="current", edge_status=AssuranceMeshEdgeStatus.edge_blocked
    )

    assert validate_assurance_mesh_edge(good_edge) is True
    assert validate_assurance_mesh_edge(bad_edge) is False

def test_compute_pressure():
    edges = [
        AssuranceMeshEdgeRecord(
            edge_id="e1", source_node_ref="n1", target_node_ref="n2", caveat_transfer_policy="keep",
            currentness_state="current", edge_status=AssuranceMeshEdgeStatus.edge_backpressured
        )
    ]

    pressure = compute_assurance_mesh_pressure(build_assurance_exchange_mesh("m1", "f"), edges)
    assert pressure.pressure_state == AssuranceMeshPressureState.moderate
    assert pressure.backpressured_edge_ratio == 1.0

def test_downgrade_paths():
    paths = [
        AssuranceMeshPathRecord(
            path_id="p1", outcome=AssuranceMeshPathOutcome.bounded_assurance_path
        )
    ]

    pressure = AssuranceMeshPressureRecord(
        pressure_state=AssuranceMeshPressureState.high,
        stale_packet_density=0.0, backpressured_edge_ratio=0.0, degraded_node_ratio=0.0,
        narrative_refresh_backlog=0, alert_density=0.0, no_safe_visibility_burden=0.0,
        audience_projection_mismatch=0.0, caveat_heavy_packet_ratio=0.0
    )

    downgraded = downgrade_assurance_paths_due_to_pressure(paths, pressure)
    assert downgraded[0].outcome == AssuranceMeshPathOutcome.review_only_assurance_path
