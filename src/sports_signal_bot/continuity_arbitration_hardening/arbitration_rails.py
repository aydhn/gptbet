import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from .contracts import (
    ContinuityArbitrationRailRecord,
    ArbitrationRailCaseRecord,
    ArbitrationRailEvidenceRecord,
    ContinuityArbitrationRailHealthRecord,
    ContinuityArbitrationRailWarningRecord
)

def build_continuity_arbitration_rail(rail_family: str, evidence: List[ArbitrationRailEvidenceRecord]) -> ContinuityArbitrationRailRecord:
    has_stale = any(not e.is_fresh for e in evidence)
    status = "rail_verified"
    warnings = []

    if has_stale:
        status = "rail_caveated"
        warnings.append("Stale evidence detected in arbitration rail.")

    return ContinuityArbitrationRailRecord(
        continuity_arbitration_rail_id=str(uuid.uuid4()),
        rail_family=rail_family,
        case_refs=[],
        input_refs=[],
        evidence_refs=[e.evidence_id for e in evidence],
        decision_refs=[],
        cap_refs=[],
        residue_refs=[],
        rail_status=status,
        warnings=warnings
    )

def open_arbitration_rail_case(case_family: str) -> ArbitrationRailCaseRecord:
    return ArbitrationRailCaseRecord(
        case_id=str(uuid.uuid4()),
        case_family=case_family,
        created_at=datetime.now(timezone.utc),
        status="open"
    )

def summarize_continuity_arbitration_rail(rail: ContinuityArbitrationRailRecord) -> Dict[str, Any]:
    return {
        "rail_id": rail.continuity_arbitration_rail_id,
        "status": rail.rail_status,
        "evidence_count": len(rail.evidence_refs),
        "warnings": rail.warnings
    }
