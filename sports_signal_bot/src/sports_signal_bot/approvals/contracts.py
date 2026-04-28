from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enum import Enum

class RequestStatus(str, Enum):
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"
    deferred = "deferred"
    expired = "expired"
    cancelled = "cancelled"
    superseded = "superseded"
    executed = "executed"
    execution_failed = "execution_failed"

class ReviewItemStatus(str, Enum):
    open = "open"
    in_review = "in_review"
    resolved = "resolved"
    expired = "expired"
    escalated = "escalated"
    blocked = "blocked"
    archived = "archived"

class OverrideStatus(str, Enum):
    active = "active"
    expired = "expired"
    revoked = "revoked"
    consumed = "consumed"
    superseded = "superseded"

class RequestType(str, Enum):
    approve_high_risk_decision = "approve_high_risk_decision"
    approve_refresh_plan = "approve_refresh_plan"
    approve_freeze_release = "approve_freeze_release"
    approve_dispatch_override = "approve_dispatch_override"
    approve_mode_switch = "approve_mode_switch"
    acknowledge_alarm = "acknowledge_alarm"
    defer_manual_review = "defer_manual_review"
    create_manual_override = "create_manual_override"
    revoke_override = "revoke_override"

class ReviewItemType(str, Enum):
    decision_review_item = "decision_review_item"
    refresh_review_item = "refresh_review_item"
    freeze_release_item = "freeze_release_item"
    dispatch_review_item = "dispatch_review_item"
    anomaly_review_item = "anomaly_review_item"
    manual_override_item = "manual_override_item"

class ApprovalScope(str, Enum):
    single_event = "single_event"
    single_request = "single_request"
    single_run = "single_run"
    sport_market_window = "sport_market_window"
    freeze_release_once = "freeze_release_once"
    slot_once = "slot_once"
    temporary_override_window = "temporary_override_window"
    system_wide_freeze = "system_wide_freeze"

class OverrideType(str, Enum):
    force_freeze = "force_freeze"
    force_degrade = "force_degrade"
    force_stable_only_mode = "force_stable_only_mode"
    allow_slot_run_once = "allow_slot_run_once"
    block_market_temporarily = "block_market_temporarily"
    force_review_only_dispatch = "force_review_only_dispatch"
    force_debug_dispatch = "force_debug_dispatch"
    suppress_noncritical_alerts = "suppress_noncritical_alerts"

class ApprovalRequestRecord(BaseModel):
    request_id: str
    request_type: RequestType
    request_scope: ApprovalScope
    target_entity_type: str
    target_entity_id: str
    sport: Optional[str] = None
    market_type: Optional[str] = None
    severity: str
    origin_component: str
    requested_action: str
    requires_manual_approval: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    rationale_summary: str
    related_run_ids: List[str] = Field(default_factory=list)
    related_event_ids: List[str] = Field(default_factory=list)
    status: RequestStatus = RequestStatus.pending_review
    warnings: List[str] = Field(default_factory=list)

class ApprovalDecisionRecord(BaseModel):
    decision_id: str
    request_id: str
    operator_id: str
    decision_type: str
    decision_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rationale_code: str
    operator_note: str
    effective_scope: ApprovalScope
    expiry_timestamp: Optional[datetime] = None
    execution_authorized: bool = False
    warnings: List[str] = Field(default_factory=list)

class ApprovalActionRecord(BaseModel):
    action_id: str
    decision_id: str
    action_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    action_type: str
    status: str

class ReviewItemRecord(BaseModel):
    review_id: str
    priority: str
    category: ReviewItemType
    title: str
    summary: str
    status: ReviewItemStatus = ReviewItemStatus.open
    assigned_operator: Optional[str] = None
    request_ref: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    due_at: Optional[datetime] = None
    risk_level: str
    related_artifacts: List[str] = Field(default_factory=list)
    suggested_actions: List[str] = Field(default_factory=list)

class ReviewQueueManifest(BaseModel):
    manifest_id: str
    generated_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    items: List[ReviewItemRecord] = Field(default_factory=list)

class ApprovalLedgerRecord(BaseModel):
    audit_id: str
    entity_type: str
    entity_id: str
    action: str
    operator_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reason_code: str
    note: str
    related_request_id: Optional[str] = None
    related_run_ids: List[str] = Field(default_factory=list)
    previous_record_hash: Optional[str] = None
    current_record_hash: Optional[str] = None

class OperatorIdentityRecord(BaseModel):
    operator_id: str
    display_name: str
    role: str
    active: bool = True
    approval_scopes: List[ApprovalScope] = Field(default_factory=list)
    note: Optional[str] = None

class OverrideScopeRecord(BaseModel):
    scope_type: ApprovalScope
    target_id: Optional[str] = None
    sport: Optional[str] = None
    market_type: Optional[str] = None

class OverrideRecord(BaseModel):
    override_id: str
    override_type: OverrideType
    status: OverrideStatus = OverrideStatus.active
    operator_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    scope: OverrideScopeRecord
    reason: str
    precedence_level: int = 0

class FreezeReleaseRequestRecord(BaseModel):
    request_id: str
    operator_id: str
    reason: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    target_component: Optional[str] = None

class FreezeReleaseDecisionRecord(BaseModel):
    decision_id: str
    request_id: str
    operator_id: str
    approved: bool
    decision_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operator_note: str

class ApprovalWorkflowManifest(BaseModel):
    manifest_id: str
    generated_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    open_review_items: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    deferred_count: int = 0
    active_override_count: int = 0
    unresolved_critical_ack_count: int = 0

class ReviewResolutionRecord(BaseModel):
    resolution_id: str
    review_id: str
    operator_id: str
    status: ReviewItemStatus
    resolution_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    note: str

class AlarmAckRecord(BaseModel):
    ack_id: str
    alarm_id: str
    operator_id: str
    ack_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    note: str

class AcknowledgementSummary(BaseModel):
    summary_id: str
    generated_at_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    unacked_critical_alarms: int = 0
    recent_acks: List[AlarmAckRecord] = Field(default_factory=list)
