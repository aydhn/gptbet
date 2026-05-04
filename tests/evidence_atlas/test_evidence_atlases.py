import pytest
from sports_signal_bot.evidence_atlas.contracts import (
    EvidenceAtlasNodeRecord,
    EvidenceAtlasEdgeRecord
)
from sports_signal_bot.evidence_atlas.evidence_atlases import (
    build_governance_evidence_atlas,
    validate_evidence_atlas_integrity,
    summarize_evidence_atlas_health,
    execute_evidence_atlas_query,
    preserve_caveats_in_atlas_results
)

def test_build_atlas():
    atlas = build_governance_evidence_atlas("a1", "governance_evidence_atlas")
    assert atlas.evidence_atlas_id == "a1"

def test_validate_integrity():
    atlas = build_governance_evidence_atlas("a1", "f")
    nodes = [
        EvidenceAtlasNodeRecord(atlas_node_id="n1", node_family="f", source_ref="s", source_family="s", currentness_state="c", applicability_scope="a", caveat_state="c"),
        EvidenceAtlasNodeRecord(atlas_node_id="n2", node_family="f", source_ref="s", source_family="s", currentness_state="c", applicability_scope="a", caveat_state="c")
    ]
    edges = [
        EvidenceAtlasEdgeRecord(atlas_edge_id="e1", source_node_ref="n1", target_node_ref="n2", relationship_family="r", freshness_state="f", caveat_transfer_policy="p", edge_status="s"),
        EvidenceAtlasEdgeRecord(atlas_edge_id="e2", source_node_ref="n1", target_node_ref="n3", relationship_family="r", freshness_state="f", caveat_transfer_policy="p", edge_status="s") # n3 is missing
    ]

    assert validate_evidence_atlas_integrity(atlas, nodes, [edges[0]]) is True
    assert validate_evidence_atlas_integrity(atlas, nodes, edges) is False

def test_summarize_health():
    atlas = build_governance_evidence_atlas("a1", "f")
    nodes = [
        EvidenceAtlasNodeRecord(atlas_node_id="n1", node_family="f", source_ref="s", source_family="s", currentness_state="stale", applicability_scope="a", caveat_state="c"),
    ]
    edges = []

    health = summarize_evidence_atlas_health(atlas, nodes, edges)
    assert health.is_healthy is False
    assert health.stale_node_count == 1

def test_execute_query():
    atlas = build_governance_evidence_atlas("a1", "f")
    nodes = [
        EvidenceAtlasNodeRecord(atlas_node_id="n1", node_family="f", source_ref="s", source_family="s", currentness_state="stale", applicability_scope="a", caveat_state="Has caveat"),
    ]

    result = execute_evidence_atlas_query(atlas, "lineage_trace_query", {"param": "val"}, nodes)
    assert result.results_stale is True
    assert result.results_caveated is True

def test_preserve_caveats_in_results():
    nodes = [
        EvidenceAtlasNodeRecord(atlas_node_id="n1", node_family="f", source_ref="s", source_family="s", currentness_state="c", applicability_scope="a", caveat_state="Caveat 1"),
        EvidenceAtlasNodeRecord(atlas_node_id="n2", node_family="f", source_ref="s", source_family="s", currentness_state="c", applicability_scope="a", caveat_state="none")
    ]

    caveats = preserve_caveats_in_atlas_results(nodes)
    assert len(caveats) == 1
    assert "Caveat 1" in caveats[0]
