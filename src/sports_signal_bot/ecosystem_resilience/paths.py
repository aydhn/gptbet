from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    MeshPathRecord,
    MeshPathOutcome,
    MeshEdgeRecord,
    MeshPressureOutcome
)

def enumerate_mesh_paths(edges: List[MeshEdgeRecord], source: str, target: str) -> List[List[MeshEdgeRecord]]:
    # Naive enumeration for demonstration
    paths = []
    for e in edges:
        if e.source_hub_ref == source and e.target_hub_ref == target:
            paths.append([e])
    return paths

def score_mesh_paths(paths: List[List[MeshEdgeRecord]]) -> List[MeshPathRecord]:
    scored_paths = []
    for i, path_edges in enumerate(paths):
        outcome = MeshPathOutcome.PREFERRED_BOUNDED_PATH
        for e in path_edges:
            if e.edge_status == "edge_blocked" or e.edge_status == "edge_superseded" or e.edge_status == "edge_expired":
                outcome = MeshPathOutcome.BLOCKED_PATH
                break
            if e.sovereignty_constraints:
                outcome = MeshPathOutcome.REVIEW_ONLY_PATH
            elif e.edge_status == "edge_degraded" and outcome != MeshPathOutcome.REVIEW_ONLY_PATH:
                outcome = MeshPathOutcome.DEGRADED_FALLBACK_PATH
            elif e.edge_status == "edge_caveated" and outcome not in [MeshPathOutcome.REVIEW_ONLY_PATH, MeshPathOutcome.DEGRADED_FALLBACK_PATH]:
                outcome = MeshPathOutcome.CAVEATED_PATH

        scored_paths.append(MeshPathRecord(
            path_id=f"path-{i}",
            edge_refs=[e.edge_id for e in path_edges],
            path_outcome=outcome,
            warnings=[]
        ))
    return scored_paths

def apply_mesh_constraints(path: MeshPathRecord, pressure: MeshPressureOutcome) -> MeshPathRecord:
    if pressure in [MeshPressureOutcome.HIGH_PRESSURE, MeshPressureOutcome.CRITICAL_PRESSURE]:
        if path.path_outcome == MeshPathOutcome.PREFERRED_BOUNDED_PATH:
            path.path_outcome = MeshPathOutcome.DEGRADED_FALLBACK_PATH
            path.warnings.append("Downgraded due to high mesh pressure.")
    return path

def select_bounded_mesh_path(scored_paths: List[MeshPathRecord]) -> MeshPathRecord:
    # Preference order
    for p in scored_paths:
        if p.path_outcome == MeshPathOutcome.PREFERRED_BOUNDED_PATH:
            return p
    for p in scored_paths:
        if p.path_outcome == MeshPathOutcome.REVIEW_ONLY_PATH:
            return p
    for p in scored_paths:
        if p.path_outcome == MeshPathOutcome.CAVEATED_PATH:
            return p
    for p in scored_paths:
        if p.path_outcome == MeshPathOutcome.DEGRADED_FALLBACK_PATH:
            return p

    return MeshPathRecord(path_id="none", edge_refs=[], path_outcome=MeshPathOutcome.NO_SAFE_MESH_PATH)

def summarize_mesh_route(path: MeshPathRecord) -> str:
    return f"Selected Path: {path.path_id}, Outcome: {path.path_outcome.value}"
