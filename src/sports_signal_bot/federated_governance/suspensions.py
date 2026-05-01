from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
from .contracts import (
    PlaneSuspensionRecord, AutonomyReductionRecord, ControlPlaneRecord, DelegationMode, PlaneHealthBand
)

def suspend_plane_if_unstable(plane: ControlPlaneRecord, reason: str) -> Optional[PlaneSuspensionRecord]:
    if plane.health == PlaneHealthBand.UNSTABLE:
        plane.active_status = False
        return PlaneSuspensionRecord(
            suspension_id=f"sus_{uuid.uuid4().hex[:8]}",
            plane_id=plane.plane_id,
            reason=reason,
            active=True
        )
    return None

def reduce_plane_autonomy(plane: ControlPlaneRecord, current_mode: DelegationMode, new_mode: DelegationMode, reason: str) -> AutonomyReductionRecord:
    return AutonomyReductionRecord(
        reduction_id=f"red_{uuid.uuid4().hex[:8]}",
        plane_id=plane.plane_id,
        previous_mode=current_mode,
        new_mode=new_mode,
        reason=reason
    )

def recover_plane_autonomy_if_safe(plane: ControlPlaneRecord, suspension: Optional[PlaneSuspensionRecord]) -> bool:
    if plane.health in [PlaneHealthBand.HEALTHY, PlaneHealthBand.NOISY]:
        if suspension:
            suspension.active = False
        plane.active_status = True
        return True
    return False
