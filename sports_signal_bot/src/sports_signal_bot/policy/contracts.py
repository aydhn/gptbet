from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PolicySignalStatus(str, Enum):
    PENDING = "pending"
    SCORED = "scored"
    WEAK_SIGNAL = "weak_signal"
    BELOW_THRESHOLD = "below_threshold"
    NO_BET_ZONE = "no_bet_zone"
    CANDIDATE = "candidate"
    APPROVED = "approved"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    INVALID = "invalid"
    EXPIRED = "expired"
    OVERRIDDEN = "overridden"


class ActionClass(str, Enum):
    NO_ACTION = "no_action"
    WATCHLIST = "watchlist"
    CANDIDATE = "candidate"
    APPROVED_CANDIDATE = "approved_candidate"
    BLOCKED_CANDIDATE = "blocked_candidate"


class OverrideReasonRecord(BaseModel):
    reason: str
    overridden_by: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


class NoBetReasonRecord(BaseModel):
    reason_code: str
    description: str
    severity: str = "medium"


class DecisionRationaleRecord(BaseModel):
    code: str
    description: str
    impact: str = "neutral"  # positive, negative, neutral, blocking


class PolicyDecisionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str

    signal_status: PolicySignalStatus
    action_class: ActionClass

    decision_score: Optional[float] = None
    policy_name: str

    rationale_codes: List[str] = Field(default_factory=list)
    no_bet_reasons: List[str] = Field(default_factory=list)
    block_reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    override_record: Optional[OverrideReasonRecord] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PolicyLifecycleRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str

    previous_status: PolicySignalStatus
    new_status: PolicySignalStatus

    transition_reason: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PolicyDiagnosticsRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str

    score_band: str
    edge_band: str
    uncertainty_band: str
    disagreement_band: str
    data_quality_band: str
    regime_risk_band: str


class PolicyManifest(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str
    policy_name: str

    total_evaluated: int = 0
    approved_count: int = 0
    candidate_count: int = 0
    watchlist_count: int = 0
    no_action_count: int = 0
    blocked_count: int = 0

    top_rationale_codes: Dict[str, int] = Field(default_factory=dict)
    no_bet_zone_reasons: Dict[str, int] = Field(default_factory=dict)
    blocked_reasons: Dict[str, int] = Field(default_factory=dict)

    decisions: List[PolicyDecisionRecord] = Field(default_factory=list)
    lifecycle_events: List[PolicyLifecycleRecord] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ActionClassRecord(BaseModel):
    signal_status: PolicySignalStatus
    mapped_action_class: ActionClass
