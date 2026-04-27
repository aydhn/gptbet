import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MessageSeverity(str, Enum):
    SILENT = "silent"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MessageType(str, Enum):
    DECISION_ALERT = "decision_alert"
    DECISION_REVIEW = "decision_review"
    RUN_SUMMARY = "run_summary"
    DAILY_DIGEST = "daily_digest"
    PIPELINE_WARNING = "pipeline_warning"
    PIPELINE_ERROR = "pipeline_error"
    CRITICAL_ALARM = "critical_alarm"
    HEALTH_NOTICE = "health_notice"
    DISPATCH_FAILURE_NOTICE = "dispatch_failure_notice"
    DRY_RUN_PREVIEW = "dry_run_preview"

class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    RENDERED = "rendered"
    SENT = "sent"
    FAILED_RETRYABLE = "failed_retryable"
    FAILED_FINAL = "failed_final"
    SUPPRESSED = "suppressed"
    DRY_RUN_ONLY = "dry_run_only"

class TelegramChannelDefinition(BaseModel):
    logical_name: str
    chat_id_env_var: str
    actual_chat_id: Optional[str] = None
    description: Optional[str] = None

class TelegramMessageRecord(BaseModel):
    message_id_local: str
    message_type: MessageType
    severity: MessageSeverity
    sport: str
    market_type: Optional[str] = None
    channel_name: str
    chat_target_alias: Optional[str] = None
    title: str
    body: str
    tags: List[str] = Field(default_factory=list)
    related_run_id: Optional[str] = None
    related_event_ids: List[str] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    delivery_status: DeliveryStatus = DeliveryStatus.QUEUED
    warnings: List[str] = Field(default_factory=list)

class DeliveryAttemptRecord(BaseModel):
    message_id_local: str
    attempt_timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    status: DeliveryStatus
    error_message: Optional[str] = None

class TelegramDispatchRecord(BaseModel):
    message: TelegramMessageRecord
    attempts: List[DeliveryAttemptRecord] = Field(default_factory=list)
    final_status: DeliveryStatus = DeliveryStatus.QUEUED

class DispatchPayloadRecord(BaseModel):
    event_id: str
    market: str
    sport: str
    decision_class: str
    signal_score: float
    edge: float
    allocated_stake: float
    rationale: str
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReviewPriorityRecord(BaseModel):
    level: str  # e.g., "high", "medium", "low"
    score: float

class ReviewReasonRecord(BaseModel):
    code: str
    description: str

class ReviewQueueRecord(BaseModel):
    review_id: str
    event_id: str
    sport: str
    market: str
    priority: ReviewPriorityRecord
    reasons: List[ReviewReasonRecord]
    signal_summary: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ReviewQueueSummary(BaseModel):
    run_id: str
    total_reviews: int
    high_priority_count: int
    items: List[ReviewQueueRecord]

class SummaryMessageRecord(BaseModel):
    run_id: str
    slot: str
    universe_size: int
    approved_count: int
    candidate_count: int
    watchlist_count: int
    fallback_count: int
    alarms_count: int
    top_decisions: List[DispatchPayloadRecord] = Field(default_factory=list)

class AlarmMessageRecord(BaseModel):
    incident_title: str
    severity: MessageSeverity
    failing_step: str
    run_id: str
    cause: str
    impacted_events_count: int
    status: str

class RoutingDecisionRecord(BaseModel):
    message_id_local: str
    message_type: MessageType
    assigned_channel: str
    rationale: str

class TelegramDispatchManifest(BaseModel):
    run_id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    total_messages_rendered: int = 0
    total_messages_sent: int = 0
    suppressed_count: int = 0
    retry_count: int = 0
    final_failures_count: int = 0
    channel_breakdown: Dict[str, int] = Field(default_factory=dict)
    severity_breakdown: Dict[str, int] = Field(default_factory=dict)
    records: List[TelegramDispatchRecord] = Field(default_factory=list)

class MessageTemplateRecord(BaseModel):
    template_name: str
    profile: str # short, standard, verbose
    format: str # markdown, html
