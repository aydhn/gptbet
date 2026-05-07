from typing import List
from .contracts import (
    GlobalContinuityDrillRecord,
    ContinuityPhaseRecord,
    ContinuityCheckpointRecord,
    ContinuityGapRecord,
    ContinuityResidueRecord,
    GlobalContinuityWarningRecord
)

def build_global_continuity_drill(drill_id: str, family: str) -> GlobalContinuityDrillRecord:
    return GlobalContinuityDrillRecord(
        global_continuity_drill_id=drill_id,
        drill_family=family,
        drill_status="continuity_rehearsed_honestly"
    )

def advance_global_continuity_phase(drill: GlobalContinuityDrillRecord, phase: ContinuityPhaseRecord) -> None:
    drill.phase_refs.append(phase)

def verify_global_continuity_checkpoint(drill: GlobalContinuityDrillRecord, checkpoint: ContinuityCheckpointRecord) -> None:
    drill.checkpoint_refs.append(checkpoint)

def summarize_global_continuity_drill(drill: GlobalContinuityDrillRecord) -> dict:
    has_residue = len(drill.residue_refs) > 0
    if has_residue and drill.drill_status == "continuity_rehearsed_honestly":
        drill.drill_status = "continuity_rehearsed_with_caveats"

    return {
        "id": drill.global_continuity_drill_id,
        "status": drill.drill_status,
        "phases_count": len(drill.phase_refs),
        "checkpoints_count": len(drill.checkpoint_refs),
        "warnings": len(drill.warnings)
    }

def create_global_continuity_checkpoint(checkpoint_id: str, family: str) -> ContinuityCheckpointRecord:
    return ContinuityCheckpointRecord(checkpoint_id=checkpoint_id, checkpoint_family=family)

def detect_global_continuity_gaps(drill: GlobalContinuityDrillRecord, gap: ContinuityGapRecord) -> None:
    drill.gap_refs.append(gap)
    drill.drill_status = "continuity_gapped"

def record_global_continuity_residue(drill: GlobalContinuityDrillRecord, residue: ContinuityResidueRecord) -> None:
    drill.residue_refs.append(residue)
