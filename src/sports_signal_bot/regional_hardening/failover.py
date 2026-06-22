# flake8: noqa: E501
import uuid
from typing import List

from .contracts import (
    FailoverCheckpointRecord,
    FailoverLagRecord,
    FailoverSourceRecord,
    FailoverTargetRecord,
    RegionalFailoverDrillInputRecord,
    RegionalFailoverDrillRecord,
    RegionalFailoverStatus,
    RegionalFailoverWarningRecord,
)


def build_regional_failover_drill(
    input_record: RegionalFailoverDrillInputRecord,
) -> RegionalFailoverDrillRecord:
    status = RegionalFailoverStatus.failover_ready
    warnings = []

    if (
        not input_record.source.freshness_marker
        or not input_record.target.readiness_marker
    ):
        status = RegionalFailoverStatus.failover_gapped
        warnings.append(
            RegionalFailoverWarningRecord(
                warning_id=str(uuid.uuid4()),
                message="Missing freshness or readiness marker",
            )
        )

    if not input_record.rollbacks or any(
        not r.readiness for r in input_record.rollbacks
    ):
        status = RegionalFailoverStatus.failover_blocked
        warnings.append(
            RegionalFailoverWarningRecord(
                warning_id=str(uuid.uuid4()), message="Rollback readiness incomplete"
            )
        )

    if any(r.is_hidden for r in input_record.residues):
        status = RegionalFailoverStatus.failover_blocked
        warnings.append(
            RegionalFailoverWarningRecord(
                warning_id=str(uuid.uuid4()), message="Hidden residues detected"
            )
        )

    return RegionalFailoverDrillRecord(
        failover_drill_id=str(uuid.uuid4()),
        drill_family=input_record.drill_family,
        source_region_ref=input_record.source,
        target_region_ref=input_record.target,
        checkpoint_refs=input_record.checkpoints,
        lag_refs=input_record.lags,
        rollback_refs=input_record.rollbacks,
        residue_refs=input_record.residues,
        failover_status=status,
        warnings=warnings,
    )


def verify_failover_source_and_target(
    source: FailoverSourceRecord, target: FailoverTargetRecord
) -> bool:
    return bool(source.freshness_marker and target.readiness_marker)


def evaluate_failover_lag(lags: List[FailoverLagRecord]) -> bool:
    return all(lag.is_visible for lag in lags)


def verify_failover_checkpoint(checkpoint: FailoverCheckpointRecord) -> bool:
    return checkpoint.status == "verified"


def summarize_regional_failover(drill: RegionalFailoverDrillRecord) -> str:
    return f"Failover Drill {drill.failover_drill_id} Status: {drill.failover_status}"
