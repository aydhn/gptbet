from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from .states import ControllerState, RefreshRiskLevel, RefreshActionFamily, ProblemClass

class RefreshProblem(BaseModel):
    problem_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    problem_class: ProblemClass
    severity: str
    component: str
    description: str
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    context: Dict[str, Any] = Field(default_factory=dict)

class RefreshAction(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family: RefreshActionFamily
    risk_level: RefreshRiskLevel
    auto_execute_allowed: bool
    requires_manual_review: bool
    reversible: bool
    parameters: Dict[str, Any] = Field(default_factory=dict)

class RefreshPlanStep(BaseModel):
    step_order: int
    action: RefreshAction
    expected_outcome: str

class RefreshPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    problem_id: str
    steps: List[RefreshPlanStep]
    risk_level: RefreshRiskLevel
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    blocked_reasons: List[str] = Field(default_factory=list)

class StateTransition(BaseModel):
    from_state: ControllerState
    to_state: ControllerState
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RefreshAttempt(BaseModel):
    attempt_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    plan_id: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    status: str = "pending" # pending, success, failed, skipped
    executed_actions: List[str] = Field(default_factory=list)
    validation_passed: bool = False
    errors: List[str] = Field(default_factory=list)

class FreezeStateRecord(BaseModel):
    freeze_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    freeze_reason: str
    freeze_scope: str
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    auto_release_policy: str
    warnings: List[str] = Field(default_factory=list)
    active: bool = True

class DegradeStateRecord(BaseModel):
    degrade_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    degrade_level: str # mild, moderate, severe
    reason: str
    triggered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True

class RefreshManifest(BaseModel):
    manifest_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    detected_problems: List[RefreshProblem]
    chosen_plan: Optional[RefreshPlan]
    attempt: Optional[RefreshAttempt]
    state_transitions: List[StateTransition]
    current_state: ControllerState
    freeze_record: Optional[FreezeStateRecord]
    degrade_record: Optional[DegradeStateRecord]
