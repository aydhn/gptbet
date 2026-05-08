from .contracts import (
    MaintenanceModeRecord, ModeFamily, ModeStatus,
    MaintenanceBoundaryRecord, MaintenanceModeWarningRecord
)
from typing import List, Dict, Any
import uuid

def build_maintenance_mode(
    family: ModeFamily,
    boundaries: List[MaintenanceBoundaryRecord]
) -> MaintenanceModeRecord:
    warnings = []

    if not boundaries:
        warnings.append(MaintenanceModeWarningRecord(warning_id=str(uuid.uuid4()), message="Maintenance mode lacks defined boundaries"))

    status = ModeStatus.mode_verified
    if warnings:
        status = ModeStatus.mode_caveated

    return MaintenanceModeRecord(
        maintenance_mode_id=str(uuid.uuid4()),
        mode_family=family,
        boundary_refs=boundaries,
        mode_status=status,
        warnings=warnings
    )

def summarize_maintenance_mode(mode: MaintenanceModeRecord) -> Dict[str, Any]:
    return {
        "mode_id": mode.maintenance_mode_id,
        "family": mode.mode_family.value,
        "status": mode.mode_status.value,
        "boundary_count": len(mode.boundary_refs),
        "warning_count": len(mode.warnings)
    }
