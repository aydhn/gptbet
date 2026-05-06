from pydantic import Field
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from .contracts import LaneFamily, LaneStatus, StageFamily, CheckpointFamily

class MigrationSourceRecord(BaseModel):
    source_id: str
    freshness_timestamp: datetime
    is_stale: bool = False
    attributes: Dict[str, str] = Field(default_factory=dict)

class MigrationTargetRecord(BaseModel):
    target_id: str
    is_ready: bool = False
    attributes: Dict[str, str] = Field(default_factory=dict)

class MigrationStageRecord(BaseModel):
    stage_id: str
    family: StageFamily
    status: str
    details: Dict[str, str] = Field(default_factory=dict)

class MigrationCheckpointRecord(BaseModel):
    checkpoint_id: str
    family: CheckpointFamily
    verified: bool = False
    details: Dict[str, str] = Field(default_factory=dict)

class MigrationRollbackRecord(BaseModel):
    rollback_id: str
    is_explicit: bool = False
    details: Dict[str, str] = Field(default_factory=dict)

class MigrationResidueRecord(BaseModel):
    residue_id: str
    description: str
    severity: str
    details: Dict[str, str] = Field(default_factory=dict)

class MigrationCutoverRecord(BaseModel):
    cutover_id: str
    is_honest: bool = False
    details: Dict[str, str] = Field(default_factory=dict)

class MigrationWarningRecord(BaseModel):
    warning_id: str
    description: str
    severity: str

class DisasterMigrationLaneRecord(BaseModel):
    migration_lane_id: str
    lane_family: LaneFamily
    source_ref: Optional[MigrationSourceRecord] = None
    target_ref: Optional[MigrationTargetRecord] = None
    stage_refs: List[MigrationStageRecord] = Field(default_factory=list)
    checkpoint_refs: List[MigrationCheckpointRecord] = Field(default_factory=list)
    rollback_refs: List[MigrationRollbackRecord] = Field(default_factory=list)
    residue_refs: List[MigrationResidueRecord] = Field(default_factory=list)
    lane_status: LaneStatus = LaneStatus.migration_gapped
    warnings: List[MigrationWarningRecord] = Field(default_factory=list)
    cutover_ref: Optional[MigrationCutoverRecord] = None

def build_disaster_migration_lane(lane_id: str, family: LaneFamily) -> DisasterMigrationLaneRecord:
    return DisasterMigrationLaneRecord(
        migration_lane_id=lane_id,
        lane_family=family,
        lane_status=LaneStatus.migration_gapped
    )

def verify_migration_source(lane: DisasterMigrationLaneRecord, source: MigrationSourceRecord) -> None:
    lane.source_ref = source
    if source.is_stale:
        lane.warnings.append(MigrationWarningRecord(
            warning_id=f"warn_stale_source_{source.source_id}",
            description="Stale source detected.",
            severity="high"
        ))
        lane.lane_status = LaneStatus.migration_blocked

def verify_migration_checkpoint(lane: DisasterMigrationLaneRecord, checkpoint: MigrationCheckpointRecord) -> None:
    lane.checkpoint_refs.append(checkpoint)
    if not checkpoint.verified:
        lane.warnings.append(MigrationWarningRecord(
            warning_id=f"warn_failed_chk_{checkpoint.checkpoint_id}",
            description=f"Checkpoint {checkpoint.family} failed.",
            severity="high"
        ))
        if lane.lane_status == LaneStatus.migration_ready:
             lane.lane_status = LaneStatus.migration_caveated

def advance_migration_stage(lane: DisasterMigrationLaneRecord, stage: MigrationStageRecord) -> None:
    lane.stage_refs.append(stage)

def evaluate_migration_cutover_honesty(lane: DisasterMigrationLaneRecord, cutover: MigrationCutoverRecord) -> None:
    lane.cutover_ref = cutover
    has_rollback = any(r.is_explicit for r in lane.rollback_refs)
    has_source = lane.source_ref and not lane.source_ref.is_stale

    # Needs explicit rollback path and valid source
    if not has_rollback or not has_source:
        cutover.is_honest = False
        lane.lane_status = LaneStatus.migration_blocked
        lane.warnings.append(MigrationWarningRecord(
            warning_id=f"warn_dishonest_cutover_{cutover.cutover_id}",
            description="Cutover attempted without explicit rollback path or with stale source.",
            severity="critical"
        ))
    else:
        cutover.is_honest = True

    if lane.residue_refs:
        if lane.lane_status in [LaneStatus.migration_ready]:
            lane.lane_status = LaneStatus.migration_caveated

def summarize_disaster_migration(lane: DisasterMigrationLaneRecord) -> Dict:
    return {
        "lane_id": lane.migration_lane_id,
        "family": lane.lane_family.value,
        "status": lane.lane_status.value,
        "warnings_count": len(lane.warnings),
        "residue_count": len(lane.residue_refs),
        "checkpoints_verified": sum(1 for c in lane.checkpoint_refs if c.verified)
    }
