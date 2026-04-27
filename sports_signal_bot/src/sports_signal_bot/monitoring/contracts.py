from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class HealthStatus(str, Enum):
    OK = "ok"
    DEGRADED = "degraded"
    FAILED = "failed"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


class HealthSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthCheckRecord(BaseModel):
    check_name: str
    component_name: str
    run_id: str
    sport: Optional[str] = None
    market_type: Optional[str] = None
    status: HealthStatus
    severity: HealthSeverity
    measured_value: Any = None
    threshold_reference: Any = None
    message: str = ""
    related_entity_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)


class ComponentHealthRecord(BaseModel):
    component_name: str
    run_id: str
    status: HealthStatus
    score: float = 0.0  # 0 to 100
    total_checks: int = 0
    failed_checks: int = 0
    degraded_checks: int = 0
    skipped_checks: int = 0
    checks: List[HealthCheckRecord] = Field(default_factory=list)


class HealthScoreRecord(BaseModel):
    run_id: str
    global_score: float = 0.0
    global_status: HealthStatus
    components: Dict[str, ComponentHealthRecord] = Field(default_factory=dict)
    missing_critical_checks: bool = False
    penalties_applied: List[str] = Field(default_factory=list)
    explanation: str = ""


class EscalationDecision(BaseModel):
    policy_name: str
    action: str
    severity: HealthSeverity
    escalate_to: str
    reason: str


class HealthAlertRecord(BaseModel):
    alert_id: str
    run_id: str
    check_name: str
    component_name: str
    severity: HealthSeverity
    message: str
    measured_value: Any = None
    escalation_decision: Optional[EscalationDecision] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EscalationRecord(BaseModel):
    run_id: str
    alerts_escalated: int
    highest_severity: HealthSeverity
    actions_taken: List[str] = Field(default_factory=list)


class MonitoringRunManifest(BaseModel):
    run_id: str
    sport: str
    market_type: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    health_score: Optional[HealthScoreRecord] = None
    total_anomalies: int = 0
    escalation_summary: Optional[EscalationRecord] = None


class AnomalySignalRecord(BaseModel):
    anomaly_id: str
    rule_name: str
    run_id: str
    severity: HealthSeverity
    measured_value: Any
    baseline_threshold: Any
    suggested_escalation: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MonitoringSummaryRecord(BaseModel):
    run_id: str
    global_score: float
    global_status: HealthStatus
    stale_entity_counts: Dict[str, int] = Field(default_factory=dict)
    anomaly_counts_by_severity: Dict[HealthSeverity, int] = Field(default_factory=dict)
    degraded_components: List[str] = Field(default_factory=list)
    escalation_counts: int = 0
    repeated_issue_summary: List[str] = Field(default_factory=list)


class FreshnessRecord(BaseModel):
    entity_name: str
    entity_type: str
    last_updated: datetime
    age_minutes: float
    is_stale: bool
    stale_threshold_minutes: float


class IncidentCandidateRecord(BaseModel):
    incident_id: str
    run_id: str
    component_name: str
    reason: str
    severity: HealthSeverity
    consecutive_failures: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HeartbeatSummary(BaseModel):
    run_id: str
    run_completed: bool
    event_universe_size: int
    final_action_summary: Dict[str, int] = Field(default_factory=dict)
    health_score: float
    degraded_components: List[str] = Field(default_factory=list)
    fallback_count: int
    dispatch_summary: str
    key_warnings_count: int


class HeartbeatRecord(BaseModel):
    run_id: str
    summary: HeartbeatSummary
    severity: HealthSeverity = HealthSeverity.INFO
    created_at: datetime = Field(default_factory=datetime.utcnow)
    message: str


class HeartbeatTemplateInput(BaseModel):
    run_id: str
    sport: str
    market_type: str
    summary: HeartbeatSummary


class HeartbeatPolicyRecord(BaseModel):
    enabled: bool = True
    channel: str = "summaries"
    escalate_on_critical: bool = True
