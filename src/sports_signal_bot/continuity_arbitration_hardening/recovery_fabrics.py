import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from .contracts import (
    SchedulerRecoveryFabricRecord,
    RecoveryFabricLaneRecord,
    RecoveryFabricPacketRecord,
    RecoveryFabricRetryRecord,
    RecoveryFabricRollbackRecord
)

def build_scheduler_recovery_fabric(fabric_family: str, packets: List[RecoveryFabricPacketRecord]) -> SchedulerRecoveryFabricRecord:
    has_stale = any(p.is_stale for p in packets)
    status = "fabric_verified"
    warnings = []

    if has_stale:
        status = "fabric_caveated"
        warnings.append("Stale packet detected in recovery fabric.")

    return SchedulerRecoveryFabricRecord(
        scheduler_recovery_fabric_id=str(uuid.uuid4()),
        fabric_family=fabric_family,
        lane_refs=[],
        path_refs=[],
        packet_refs=[p.packet_id for p in packets],
        retry_refs=[],
        rollback_refs=[],
        gap_refs=[],
        residue_refs=[],
        fabric_status=status,
        warnings=warnings
    )

def build_recovery_fabric_packet(payload_hash: str, is_stale: bool) -> RecoveryFabricPacketRecord:
    return RecoveryFabricPacketRecord(
        packet_id=str(uuid.uuid4()),
        payload_hash=payload_hash,
        is_stale=is_stale
    )

def summarize_scheduler_recovery_fabric(fabric: SchedulerRecoveryFabricRecord) -> Dict[str, Any]:
    return {
        "fabric_id": fabric.scheduler_recovery_fabric_id,
        "status": fabric.fabric_status,
        "packet_count": len(fabric.packet_refs),
        "warnings": fabric.warnings
    }
