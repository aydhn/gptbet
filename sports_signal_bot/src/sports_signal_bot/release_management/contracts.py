from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.release_management.channels import ReleaseChannel


class PromotionRiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class CanaryResult(str, Enum):
    pass_ = "pass"
    pass_with_warnings = "pass_with_warnings"
    fail = "fail"
    inconclusive = "inconclusive"


class RequestType(str, Enum):
    promote_candidate_to_canary = "promote_candidate_to_canary"
    promote_canary_to_stable = "promote_canary_to_stable"
    promote_candidate_to_stable_direct = "promote_candidate_to_stable_direct"
    rollback_to_previous_stable = "rollback_to_previous_stable"
    quarantine_artifact = "quarantine_artifact"
    freeze_release_channel = "freeze_release_channel"
    unfreeze_release_channel = "unfreeze_release_channel"
    promote_stable_fallback_chain = "promote_stable_fallback_chain"
    mark_candidate_superseded = "mark_candidate_superseded"


class ArtifactReleaseRecord(BaseModel):
    artifact_id: str
    artifact_family: str
    artifact_version: str
    sport: str
    market_type: str
    run_id: str
    current_channel: ReleaseChannel
    target_channel: Optional[ReleaseChannel] = None
    chain_group_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    promoted_at: Optional[datetime] = None
    release_status: str
    warnings: List[str] = Field(default_factory=list)


class ReleaseChannelRecord(BaseModel):
    channel: ReleaseChannel
    active_chain_group_id: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChannelStateRecord(BaseModel):
    sport: str
    market_type: str
    active_stable_chain_id: Optional[str] = None
    active_canary_chain_id: Optional[str] = None
    last_known_good_chain_id: Optional[str] = None
    previous_stable_chain_id: Optional[str] = None
    active_candidate_chains: List[str] = Field(default_factory=list)
    frozen_channel_flags: Dict[str, bool] = Field(default_factory=dict)
    quarantined_artifacts: List[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromotionRequestRecord(BaseModel):
    request_id: str
    request_type: RequestType
    sport: str
    market_type: str
    source_chain_group_id: Optional[str] = None
    target_chain_group_id: Optional[str] = None
    target_artifact_id: Optional[str] = None
    requested_by: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str
    risk_level: PromotionRiskLevel = PromotionRiskLevel.medium
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PromotionGuardRecord(BaseModel):
    guard_name: str
    passed: bool
    reason: str
    severity: str = "critical"


class PromotionDecisionRecord(BaseModel):
    decision_id: str
    request_id: str
    decision: str
    rationale: str
    guards_evaluated: List[PromotionGuardRecord] = Field(default_factory=list)
    decision_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    requires_approval: bool = False
    approval_status: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)


class PromotionStepRecord(BaseModel):
    step_id: str
    action: str
    target_artifact_id: Optional[str] = None
    target_chain_group_id: Optional[str] = None
    target_channel: ReleaseChannel
    status: str = "pending"
    execution_time: Optional[datetime] = None
    error: Optional[str] = None


class PromotionPlanRecord(BaseModel):
    plan_id: str
    decision_id: str
    steps: List[PromotionStepRecord] = Field(default_factory=list)
    status: str = "created"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CanaryScopeRecord(BaseModel):
    slots: List[str] = Field(default_factory=list)
    sports: List[str] = Field(default_factory=list)
    markets: List[str] = Field(default_factory=list)
    percentage: Optional[float] = None


class CanaryComparisonRecord(BaseModel):
    metric_name: str
    canary_value: float
    stable_value: float
    delta: float
    threshold: float
    passed: bool


class CanaryHealthSnapshot(BaseModel):
    health_score: float
    anomalies: int
    warnings: List[str] = Field(default_factory=list)


class CanaryPromotionGateRecord(BaseModel):
    gate_name: str
    passed: bool
    reason: str


class CanaryValidationRecord(BaseModel):
    validation_id: str
    run_id: str
    canary_chain_id: str
    stable_chain_id: str
    comparisons: List[CanaryComparisonRecord] = Field(default_factory=list)
    health: CanaryHealthSnapshot
    gates: List[CanaryPromotionGateRecord] = Field(default_factory=list)
    result: CanaryResult
    validated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CanaryRunRecord(BaseModel):
    canary_run_id: str
    request_id: str
    chain_group_id: str
    scope: CanaryScopeRecord
    status: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    validation: Optional[CanaryValidationRecord] = None


class RollbackTargetRecord(BaseModel):
    chain_group_id: str
    reason: str
    known_safe: bool


class RollbackValidationRecord(BaseModel):
    target_valid: bool
    checks_passed: List[str] = Field(default_factory=list)
    checks_failed: List[str] = Field(default_factory=list)


class RollbackExecutionRecord(BaseModel):
    execution_id: str
    plan_id: str
    status: str
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    log: List[str] = Field(default_factory=list)


class RollbackPlanRecord(BaseModel):
    plan_id: str
    sport: str
    market_type: str
    source_chain_group_id: str
    target: RollbackTargetRecord
    approval_required: bool = False
    validation: RollbackValidationRecord
    execution: Optional[RollbackExecutionRecord] = None


class RollbackDecisionRecord(BaseModel):
    decision_id: str
    sport: str
    market_type: str
    approved: bool
    reason: str
    plan: Optional[RollbackPlanRecord] = None


class ReleaseLedgerRecord(BaseModel):
    release_event_id: str
    action: str
    target_channel: Optional[ReleaseChannel] = None
    source_channel: Optional[ReleaseChannel] = None
    chain_group_id: Optional[str] = None
    artifact_id: Optional[str] = None
    operator: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale: str
    related_requests: List[str] = Field(default_factory=list)


class ReleaseManifest(BaseModel):
    manifest_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_stable_chains: Dict[str, str] = Field(default_factory=dict)
    active_canary_chains: Dict[str, str] = Field(default_factory=dict)
    pending_promotions: int = 0
    canary_pass_count: int = 0
    canary_fail_count: int = 0
    rollback_count: int = 0
    quarantined_artifacts: int = 0
    frozen_channels: List[str] = Field(default_factory=list)
    recent_ledger_entries: List[ReleaseLedgerRecord] = Field(default_factory=list)
