import pytest
from datetime import datetime, timezone
from sports_signal_bot.overlay_mesh_governance import (
    build_overlay_exchange_mesh,
    add_overlay_mesh_node,
    add_overlay_mesh_edge,
    propagate_overlay_across_mesh,
    OverlayMeshPathRecord,
    OverlayMeshCaveatRecord,
    PropagationDimensionRecord,
    OverlayMeshNodeRecord,
    OverlayMeshEdgeRecord,
    OverlayMeshCurrentnessRecord
)

def test_propagate_overlay():
    mesh = build_overlay_exchange_mesh("mesh_1", "bounded_projection_overlay_mesh", "pol_1", "pol_1", "pol_1")
    path = OverlayMeshPathRecord(
        path_id="path_1",
        node_sequence=["node_1", "node_2"],
        edge_sequence=["edge_1"],
        path_caveats=[OverlayMeshCaveatRecord(caveat_id="c1", caveat_description="test", caveat_source="test")],
        path_status="active"
    )
    dim = PropagationDimensionRecord(dimension_name="test", dimension_value="test")
    res = propagate_overlay_across_mesh("ov_1", path, [dim])
    assert res.target_visibility_result.visibility_status == "propagated_bounded"
    assert len(res.preserved_caveats) == 1
    assert res.currentness_decay.decay_amount > 0

def test_propagate_overlay_blocked():
    path = OverlayMeshPathRecord(
        path_id="path_2",
        node_sequence=["node_1", "node_2"],
        edge_sequence=["edge_1"],
        path_caveats=[],
        path_status="blocked"
    )
    res = propagate_overlay_across_mesh("ov_2", path, [])
    assert res.target_visibility_result.visibility_status == "propagated_blocked"

def test_propagate_overlay_review_only():
    path = OverlayMeshPathRecord(
        path_id="path_3",
        node_sequence=["node_1"],
        edge_sequence=[],
        path_caveats=[OverlayMeshCaveatRecord(caveat_id="c2", caveat_description="test", caveat_source="review_only")],
        path_status="active"
    )
    res = propagate_overlay_across_mesh("ov_3", path, [])
    assert res.target_visibility_result.visibility_status == "propagated_review_only"
