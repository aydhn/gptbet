from typing import List, Optional
import uuid
from .contracts import (
    RegionalFailoverDrillRecord, FailoverSourceRecord, FailoverTargetRecord,
    FailoverCheckpointRecord, FailoverLagRecord, FailoverRollbackRecord,
    FailoverResidueRecord, RegionalFailoverStatus, RegionalFailoverDrillFamily,
    RegionalFailoverWarningRecord
)

def build_regional_failover_drill(
    drill_family: RegionalFailoverDrillFamily,
    source: FailoverSourceRecord,
    target: FailoverTargetRecord,
    checkpoints: List[FailoverCheckpointRecord],
    lags: List[FailoverLagRecord],
    rollbacks: List[FailoverRollbackRecord],
    residues: List[FailoverResidueRecord]
) -> RegionalFailoverDrillRecord:
    status = RegionalFailoverStatus.failover_ready
    warnings = []

    if not source.freshness_marker or not target.readiness_marker:
        status = RegionalFailoverStatus.failover_gapped
        warnings.append(RegionalFailoverWarningRecord(warning_id=str(uuid.uuid4()), message="Missing freshness or readiness marker"))

    if not rollbacks or any(not r.readiness for r in rollbacks):
        status = RegionalFailoverStatus.failover_blocked
        warnings.append(RegionalFailoverWarningRecord(warning_id=str(uuid.uuid4()), message="Rollback readiness incomplete"))

    if any(r.is_hidden for r in residues):
        status = RegionalFailoverStatus.failover_blocked
        warnings.append(RegionalFailoverWarningRecord(warning_id=str(uuid.uuid4()), message="Hidden residues detected"))

    return RegionalFailoverDrillRecord(
        failover_drill_id=str(uuid.uuid4()),
        drill_family=drill_family,
        source_region_ref=source,
        target_region_ref=target,
        checkpoint_refs=checkpoints,
        lag_refs=lags,
        rollback_refs=rollbacks,
        residue_refs=residues,
        failover_status=status,
        warnings=warnings
    )

def verify_failover_source_and_target(source: FailoverSourceRecord, target: FailoverTargetRecord) -> bool:
    return bool(source.freshness_marker and target.readiness_marker)

def evaluate_failover_lag(lags: List[FailoverLagRecord]) -> bool:
    return all(l.is_visible for l in lags)

def verify_failover_checkpoint(checkpoint: FailoverCheckpointRecord) -> bool:
    return checkpoint.status == "verified"

def summarize_regional_failover(drill: RegionalFailoverDrillRecord) -> str:
    return f"Failover Drill {drill.failover_drill_id} Status: {drill.failover_status}"
