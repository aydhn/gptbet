from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
from .contracts import (
    ControlPlaneRecord, DelegationMode, DelegatedActionRecord,
    DelegatedActionLedgerRecord, DelegationDenialRecord, DelegationThrottleRecord,
    DelegationPolicyRecord
)

def record_delegated_action(plane_id: str, delegation_id: str, payload: Dict[str, Any]) -> DelegatedActionRecord:
    return DelegatedActionRecord(
        action_id=f"act_{uuid.uuid4().hex[:8]}",
        plane_id=plane_id,
        delegation_id=delegation_id,
        payload=payload,
        status="proposed"
    )

def record_delegation_denial(delegation_id: str, reason: str) -> DelegationDenialRecord:
    return DelegationDenialRecord(
        denial_id=f"den_{uuid.uuid4().hex[:8]}",
        delegation_id=delegation_id,
        reason=reason
    )

def summarize_delegation_usage(actions: List[DelegatedActionRecord]) -> Dict[str, int]:
    summary = {}
    for a in actions:
        summary[a.plane_id] = summary.get(a.plane_id, 0) + 1
    return summary

def detect_overactive_plane(actions: List[DelegatedActionRecord], threshold: int = 10) -> List[str]:
    usage = summarize_delegation_usage(actions)
    return [plane_id for plane_id, count in usage.items() if count > threshold]

def throttle_plane_delegation(plane_id: str, reason: str) -> DelegationThrottleRecord:
    return DelegationThrottleRecord(
        throttle_id=f"thr_{uuid.uuid4().hex[:8]}",
        plane_id=plane_id,
        reason=reason,
        active=True
    )
