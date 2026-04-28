import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Callable

class JobState(str, Enum):
    planned = "planned"
    ready = "ready"
    blocked_by_dependency = "blocked_by_dependency"
    blocked_by_state = "blocked_by_state"
    approval_pending = "approval_pending"
    running = "running"
    succeeded = "succeeded"
    succeeded_with_warnings = "succeeded_with_warnings"
    failed_retryable = "failed_retryable"
    failed_final = "failed_final"
    skipped = "skipped"
    deferred = "deferred"
    cancelled = "cancelled"
    superseded = "superseded"
    dry_run_only = "dry_run_only"

class SlotType(str, Enum):
    morning = "morning"
    midday = "midday"
    evening = "evening"
    night_maintenance = "night_maintenance"
    custom = "custom"

class SchedulerMode(str, Enum):
    dry_run = "dry_run"
    planned_only = "planned_only"
    execute = "execute"
    execute_with_safe_degrade = "execute_with_safe_degrade"
    recovery_mode = "recovery_mode"

class JobDependencyRecord(BaseModel):
    dependency_job_name: str
    dependency_type: str = "hard" # hard, soft, freshness, approval, completion, optional
    required_state: JobState = JobState.succeeded

class ScheduledJobDefinition(BaseModel):
    job_name: str
    job_family: str
    description: str = ""
    enabled: bool = True
    priority: int = 10
    execution_mode: str = "auto"
    allowed_slots: List[SlotType] = Field(default_factory=lambda: [SlotType.morning, SlotType.midday, SlotType.evening, SlotType.night_maintenance])
    dependency_names: List[str] = Field(default_factory=list)
    preconditions: List[str] = Field(default_factory=list)
    postconditions: List[str] = Field(default_factory=list)
    retry_policy_name: str = "no_retry"
    freeze_behavior: str = "block"
    degrade_behavior: str = "safe_mode"
    requires_approval_scope: Optional[str] = None
    job_runner_entrypoint: str
    output_contract_name: str

class SlotScheduleRecord(BaseModel):
    slot_id: str
    slot_type: SlotType
    date: datetime.date
    timezone: str = "UTC"
    start_time: datetime.time
    end_time: datetime.time
    allowed_job_families: List[str] = Field(default_factory=lambda: ["all"])

class SchedulerRunContext(BaseModel):
    schedule_run_id: str
    slot: SlotScheduleRecord
    mode: SchedulerMode = SchedulerMode.execute
    system_state: Dict[str, Any] = Field(default_factory=dict)

class JobStateTransitionRecord(BaseModel):
    job_name: str
    timestamp: datetime.datetime
    from_state: JobState
    to_state: JobState
    reason: str

class JobExecutionAttemptRecord(BaseModel):
    attempt_id: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    result: str = "unknown"
    error: Optional[str] = None

class ScheduledExecutionRecord(BaseModel):
    schedule_run_id: str
    job_name: str
    slot_id: str
    date: datetime.date
    planned_time: datetime.datetime
    actual_start: Optional[datetime.datetime] = None
    actual_end: Optional[datetime.datetime] = None
    state_before: JobState = JobState.planned
    state_after: JobState = JobState.planned
    dependency_status: str = "resolved"
    retry_count: int = 0
    run_result: str = "pending"
    warnings: List[str] = Field(default_factory=list)
    related_manifest_paths: List[str] = Field(default_factory=list)
    operator_context: Optional[Dict[str, Any]] = None

class RunbookRecord(BaseModel):
    runbook_name: str
    purpose: str
    ordered_job_steps: List[str]
    normal_path: List[str]
    degraded_path: List[str]
    freeze_path: List[str]
    operator_notes: str
    expected_outputs: List[str]
    escalation_hints: str

class SchedulerSummaryRecord(BaseModel):
    planned_jobs: int = 0
    executed_jobs: int = 0
    skipped_jobs: int = 0
    deferred_jobs: int = 0
    failed_jobs: int = 0
    retry_counts: int = 0
    blocked_by_dependency_counts: int = 0
    blocked_by_state_counts: int = 0
    runbook_outcome_summary: str = ""

class SchedulerManifest(BaseModel):
    schedule_run_id: str
    slot_id: str
    mode: SchedulerMode
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    summary: SchedulerSummaryRecord
    executions: List[ScheduledExecutionRecord] = Field(default_factory=list)
    transitions: List[JobStateTransitionRecord] = Field(default_factory=list)

class JobPreconditionRecord(BaseModel):
    check_name: str
    passed: bool
    reason: str

class JobPostconditionRecord(BaseModel):
    check_name: str
    passed: bool
    reason: str

class CatchupWindowRecord(BaseModel):
    policy_name: str
    missed_slots: List[str]
    relevance_window_hours: int

class RetryDecisionRecord(BaseModel):
    job_name: str
    attempt_number: int
    will_retry: bool
    delay_seconds: int
    reason: str
