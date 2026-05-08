from .contracts import LifecycleMatrixRow
from typing import List, Dict, Any

def build_terminal_lifecycle_matrix(rows: List[LifecycleMatrixRow]) -> Dict[str, Any]:
    return {
        "rows": rows,
        "matrix_status": "built"
    }

def validate_terminal_lifecycle_row(row: LifecycleMatrixRow) -> bool:
    return (
        row.owner_visible and
        row.freshness_note_visible and
        row.no_safe_visible and
        row.sovereignty_note_visible and
        row.residue_visible and
        row.degraded_lane_visible and
        row.replayability_preserved and
        row.lineage_preserved and
        row.rollback_explicit and
        row.deprecation_state_explicit and
        row.maintenance_boundary_explicit and
        row.stewardship_cadence_explicit and
        row.acceptance_carry_forward_explicit
    )

def summarize_terminal_lifecycle_matrix(rows: List[LifecycleMatrixRow]) -> Dict[str, Any]:
    valid_rows = [r for r in rows if validate_terminal_lifecycle_row(r)]
    return {
        "total_rows": len(rows),
        "valid_rows": len(valid_rows),
        "invalid_rows": len(rows) - len(valid_rows)
    }
