from typing import List, Dict, Any, Optional
from sports_signal_bot.overlay_mesh_governance.contracts import (
    OverlayMeshPropagationRecord,
    OverlayMeshPathRecord,
    OverlayMeshCaveatRecord,
    PropagationDimensionRecord,
    PropagationDecayRecord,
    PropagationVisibilityDecisionRecord,
    OverlayMeshCurrentnessRecord,
    PropagationReplaySupportRecord
)

def propagate_overlay_across_mesh(
    source_overlay_ref: str,
    path: OverlayMeshPathRecord,
    dimensions: List[PropagationDimensionRecord]
) -> OverlayMeshPropagationRecord:

    # Check if propagation is blocked
    if path.path_status == "blocked":
        visibility = PropagationVisibilityDecisionRecord(visibility_status="propagated_blocked", reasons=["Path is blocked"])
        return OverlayMeshPropagationRecord(
            propagation_id=f"prop_{source_overlay_ref}_{path.path_id}",
            source_overlay_ref=source_overlay_ref,
            propagation_path=path,
            projected_dimensions=dimensions,
            preserved_caveats=path.path_caveats,
            currentness_decay=PropagationDecayRecord(decay_reason="blocked", decay_amount=1.0),
            replay_support_refs=[],
            downgrade_reasons=["Path blocked"],
            target_visibility_result=visibility
        )

    visibility = PropagationVisibilityDecisionRecord(visibility_status="propagated_bounded", reasons=[])

    if "review_only" in [c.caveat_source for c in path.path_caveats]:
        visibility.visibility_status = "propagated_review_only"

    decay = decay_overlay_projection_by_path(path)

    return OverlayMeshPropagationRecord(
        propagation_id=f"prop_{source_overlay_ref}_{path.path_id}",
        source_overlay_ref=source_overlay_ref,
        propagation_path=path,
        projected_dimensions=dimensions,
        preserved_caveats=preserve_caveats_across_mesh(path),
        currentness_decay=decay,
        replay_support_refs=[],
        downgrade_reasons=[],
        target_visibility_result=visibility
    )

def decay_overlay_projection_by_path(path: OverlayMeshPathRecord) -> PropagationDecayRecord:
    decay_amount = 0.05 * len(path.edge_sequence)
    return PropagationDecayRecord(decay_reason="path_length", decay_amount=decay_amount)

def preserve_caveats_across_mesh(path: OverlayMeshPathRecord) -> List[OverlayMeshCaveatRecord]:
    # All caveats must be preserved
    return path.path_caveats

def summarize_propagation_result(propagation: OverlayMeshPropagationRecord) -> Dict[str, Any]:
    return {
        "propagation_id": propagation.propagation_id,
        "status": propagation.target_visibility_result.visibility_status,
        "caveat_count": len(propagation.preserved_caveats),
        "decay_amount": propagation.currentness_decay.decay_amount
    }
