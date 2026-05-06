from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

class LaneFamily(str, Enum):
    archive_to_archive_migration_lane = "archive_to_archive_migration_lane"
    archive_to_runtime_recovery_lane = "archive_to_runtime_recovery_lane"
    degraded_continuity_migration_lane = "degraded_continuity_migration_lane"
    trace_context_migration_lane = "trace_context_migration_lane"
    assurance_surface_migration_lane = "assurance_surface_migration_lane"
    review_surface_migration_lane = "review_surface_migration_lane"
    mixed_disaster_migration_lane = "mixed_disaster_migration_lane"

class LaneStatus(str, Enum):
    migration_ready = "migration_ready"
    migration_caveated = "migration_caveated"
    migration_review_only = "migration_review_only"
    migration_gapped = "migration_gapped"
    migration_blocked = "migration_blocked"
    migration_overclaimed = "migration_overclaimed"

class StageFamily(str, Enum):
    source_verification_stage = "source_verification_stage"
    archive_lineage_stage = "archive_lineage_stage"
    transfer_stage = "transfer_stage"
    target_validation_stage = "target_validation_stage"
    cutover_stage = "cutover_stage"
    rollback_readiness_stage = "rollback_readiness_stage"
    residue_capture_stage = "residue_capture_stage"
    end_of_lane_review_stage = "end_of_lane_review_stage"

class CheckpointFamily(str, Enum):
    source_freshness_verified_checkpoint = "source_freshness_verified_checkpoint"
    lineage_continuity_verified_checkpoint = "lineage_continuity_verified_checkpoint"
    no_safe_visibility_verified_checkpoint = "no_safe_visibility_verified_checkpoint"
    sovereignty_visibility_verified_checkpoint = "sovereignty_visibility_verified_checkpoint"
    target_integrity_verified_checkpoint = "target_integrity_verified_checkpoint"
    rollback_path_verified_checkpoint = "rollback_path_verified_checkpoint"
    residue_recorded_checkpoint = "residue_recorded_checkpoint"
    cutover_honesty_verified_checkpoint = "cutover_honesty_verified_checkpoint"

class DrillFamily(str, Enum):
    operator_reviewer_coordination_drill = "operator_reviewer_coordination_drill"
    operator_incident_owner_drill = "operator_incident_owner_drill"
    archive_restore_coordination_drill = "archive_restore_coordination_drill"
    sovereignty_visibility_coordination_drill = "sovereignty_visibility_coordination_drill"
    no_safe_visibility_coordination_drill = "no_safe_visibility_coordination_drill"
    multi_surface_disaster_coordination_drill = "multi_surface_disaster_coordination_drill"
    executive_visibility_coordination_drill = "executive_visibility_coordination_drill"
    mixed_team_handoff_drill = "mixed_team_handoff_drill"

class ReadinessStatus(str, Enum):
    coordination_verified = "coordination_verified"
    coordination_caveated = "coordination_caveated"
    coordination_review_only = "coordination_review_only"
    coordination_gapped = "coordination_gapped"
    coordination_blocked = "coordination_blocked"

class ChainFamily(str, Enum):
    archive_restore_chain = "archive_restore_chain"
    archive_to_context_chain = "archive_to_context_chain"
    archive_to_assurance_chain = "archive_to_assurance_chain"
    archive_to_review_chain = "archive_to_review_chain"
    trace_restore_chain = "trace_restore_chain"
    proof_restore_chain = "proof_restore_chain"
    composite_archival_recovery_chain = "composite_archival_recovery_chain"

class ChainStatus(str, Enum):
    chain_verified = "chain_verified"
    chain_caveated = "chain_caveated"
    chain_review_only = "chain_review_only"
    chain_gapped = "chain_gapped"
    chain_broken = "chain_broken"
    chain_overclaimed = "chain_overclaimed"

class WarGameFamily(str, Enum):
    no_safe_visibility_war_game = "no_safe_visibility_war_game"
    sovereignty_visibility_war_game = "sovereignty_visibility_war_game"
    degraded_lane_visibility_war_game = "degraded_lane_visibility_war_game"
    archive_visibility_war_game = "archive_visibility_war_game"
    executive_summary_visibility_war_game = "executive_summary_visibility_war_game"
    mixed_failure_visibility_war_game = "mixed_failure_visibility_war_game"
    cross_team_visibility_war_game = "cross_team_visibility_war_game"
    continuity_visibility_war_game = "continuity_visibility_war_game"

class WarGameStatus(str, Enum):
    visibility_preserved = "visibility_preserved"
    visibility_caveated = "visibility_caveated"
    visibility_review_only = "visibility_review_only"
    visibility_lost = "visibility_lost"
    visibility_overclaimed = "visibility_overclaimed"
    war_game_blocked = "war_game_blocked"

# ... (Records will be defined in respective modules for simplicity, or we can put them all here. Let's put base models here.)

class BaseRecord(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class TeamOwnerRecord(BaseModel):
    owner_id: str
    name: str

class HandoffWindowRecord(BaseModel):
    window_id: str
    max_duration_seconds: int

class RecoveryChainRestoreRecord(BaseModel):
    restore_id: str
    successful: bool

class VisibilityMarkerRecord(BaseModel):
    marker_id: str
    is_suppressed: bool


class RecoveryChainDiffRecord(BaseModel):
    diff_id: str
    description: str

class VisibilitySuppressionRecord(BaseModel):
    suppression_id: str
    description: str
