from pydantic import BaseModel, Field
from typing import List, Dict

class OperationalVisibilityMatrixRow(BaseModel):
    row_id: str
    surface_name: str
    owner_visible: bool = False
    freshness_note_visible: bool = False
    no_safe_visible: bool = False
    sovereignty_note_visible: bool = False
    residue_visible: bool = False
    degraded_lane_visible: bool = False
    replayability_preserved: bool = False
    archive_continuity_preserved: bool = False
    handoff_explicit: bool = False
    rollback_explicit: bool = False

class OperationalVisibilityMatrix(BaseModel):
    matrix_id: str
    rows: List[OperationalVisibilityMatrixRow] = Field(default_factory=list)

def build_operational_visibility_matrix(matrix_id: str) -> OperationalVisibilityMatrix:
    return OperationalVisibilityMatrix(matrix_id=matrix_id)

def validate_operational_visibility_row(matrix: OperationalVisibilityMatrix, row: OperationalVisibilityMatrixRow) -> None:
    matrix.rows.append(row)

def summarize_operational_visibility_matrix(matrix: OperationalVisibilityMatrix) -> Dict:
    return {
        "matrix_id": matrix.matrix_id,
        "total_rows": len(matrix.rows),
        "fully_visible": sum(1 for r in matrix.rows if r.owner_visible and r.no_safe_visible and r.sovereignty_note_visible)
    }
