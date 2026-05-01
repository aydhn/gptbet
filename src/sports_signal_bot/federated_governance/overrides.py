from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime, timedelta
from .contracts import (
    EmergencyOverrideRecord, OverrideExpiryRecord, ControlPlaneRecord
)

def issue_emergency_override(issuer: str, target: Optional[str], action: str, reason: str) -> EmergencyOverrideRecord:
    return EmergencyOverrideRecord(
        override_id=f"ovr_{uuid.uuid4().hex[:8]}",
        issuer_plane_id=issuer,
        target_plane_id=target,
        action=action,
        reason=reason
    )

def expire_emergency_override(override: EmergencyOverrideRecord) -> OverrideExpiryRecord:
    override.active = False
    return OverrideExpiryRecord(
        expiry_id=f"exp_{uuid.uuid4().hex[:8]}",
        override_id=override.override_id,
        expires_at=datetime.utcnow()
    )

def enforce_override_precedence(override: EmergencyOverrideRecord, target_plane: ControlPlaneRecord) -> bool:
    if not override.active:
        return False
    if override.target_plane_id and override.target_plane_id != target_plane.plane_id:
        return False
    return True

def explain_override_effect_on_planes(override: EmergencyOverrideRecord, planes: List[ControlPlaneRecord]) -> str:
    affected = [p.plane_id for p in planes if enforce_override_precedence(override, p)]
    return f"Override {override.override_id} ({override.action}) affects planes: {', '.join(affected)}"
