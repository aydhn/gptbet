from .contracts import (
    DeprecationMapRecord, MapFamily, MapStatus,
    DeprecationSurfaceRecord, DeprecationStateRecord,
    DeprecationMapWarningRecord, StateFamily
)
from typing import List, Dict, Any
import uuid

def build_deprecation_map(
    family: MapFamily,
    surfaces: List[DeprecationSurfaceRecord],
    states: List[DeprecationStateRecord]
) -> DeprecationMapRecord:
    warnings = []

    # silent deprecation yasak
    if not states:
         warnings.append(DeprecationMapWarningRecord(warning_id=str(uuid.uuid4()), message="No deprecation states provided"))

    status = MapStatus.map_verified
    if warnings:
        status = MapStatus.map_caveated

    return DeprecationMapRecord(
        deprecation_map_id=str(uuid.uuid4()),
        map_family=family,
        surface_refs=surfaces,
        state_refs=states,
        map_status=status,
        warnings=warnings
    )

def summarize_deprecation_map(map_record: DeprecationMapRecord) -> Dict[str, Any]:
    return {
        "map_id": map_record.deprecation_map_id,
        "family": map_record.map_family.value,
        "status": map_record.map_status.value,
        "surface_count": len(map_record.surface_refs),
        "state_count": len(map_record.state_refs),
        "warning_count": len(map_record.warnings)
    }
