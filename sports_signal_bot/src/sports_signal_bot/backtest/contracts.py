from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


class SettlementStatus(str, Enum):
    SETTLED_WIN = "settled_win"
    SETTLED_LOSS = "settled_loss"
    SETTLED_VOID = "settled_void"
    SETTLED_PUSH = "settled_push"
    UNSETTLED_PENDING = "unsettled_pending"
    UNSUPPORTED_SETTLEMENT = "unsupported_settlement"
    INVALID_RESULT = "invalid_result"


class ExecutionEligibility(str, Enum):
    EXECUTABLE = "executable"
    SKIPPED_POLICY = "skipped_policy"
    SKIPPED_WATCHLIST = "skipped_watchlist"
    INVALID_CLASS = "invalid_class"
    BLOCKED = "blocked"


class ExecutionEligibilityRecord(BaseModel):
    eligibility: ExecutionEligibility
    reason: str


class SettlementRecord(BaseModel):
    status: SettlementStatus
    realized_outcome: Optional[str] = None
    hit_flag: Optional[bool] = None
    probabilistic_loss: Optional[float] = None
    notes: Optional[str] = None
    processed_at_utc: datetime = Field(default_factory=datetime.utcnow)


class BacktestDecisionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    event_datetime_utc: datetime
    decision_timestamp_utc: datetime

    selection: str
    signal_status: PolicySignalStatus
    action_class: ActionClass

    final_probability: Optional[float] = None
    market_implied_probability: Optional[float] = None
    signal_score: Optional[float] = None

    threshold_policy_name: str
    policy_name: str

    edge_snapshot: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)


class BacktestLedgerRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    event_datetime_utc: datetime
    decision_timestamp_utc: datetime

    signal_status: PolicySignalStatus
    action_class: ActionClass

    executed_flag: bool
    execution_reason: str

    selection: str
    final_probability: Optional[float] = None
    market_implied_probability: Optional[float] = None
    signal_score: Optional[float] = None

    threshold_policy_name: str
    policy_name: str

    result_status: SettlementStatus
    realized_outcome: Optional[str] = None
    hit_flag: Optional[bool] = None
    probabilistic_loss: Optional[float] = None

    edge_snapshot: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)
    run_id: str

    stake_units: Optional[float] = None
    payout_multiplier: Optional[float] = None
    pnl_units: Optional[float] = None


class BacktestReplayRecord(BaseModel):
    decision: BacktestDecisionRecord
    eligibility: ExecutionEligibilityRecord
    settlement: SettlementRecord


class ActionSubsetSummary(BaseModel):
    subset_name: str
    total_decisions: int = 0
    executed_decisions: int = 0
    skipped_decisions: int = 0
    win_count: int = 0
    loss_count: int = 0
    void_count: int = 0
    hit_rate: Optional[float] = None
    average_signal_score: Optional[float] = None
    average_edge_snapshot: Optional[float] = None


class BacktestPeriodSummary(BaseModel):
    period_label: str
    start_date: datetime
    end_date: datetime

    executed_count: int = 0
    hit_rate: Optional[float] = None
    avg_score: Optional[float] = None
    avg_edge: Optional[float] = None
    void_count: int = 0
    warnings: List[str] = Field(default_factory=list)


class ReplayWindowDefinition(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    window_type: str = "full-history"


class ReplayWindowRecord(BaseModel):
    definition: ReplayWindowDefinition
    total_evaluated: int = 0
    execution_rate: float = 0.0


class BacktestSummaryRecord(BaseModel):
    run_id: str
    sport: str
    market: str
    total_decisions: int = 0
    executed_decisions: int = 0
    skipped_decisions: int = 0
    win_count: int = 0
    loss_count: int = 0
    void_count: int = 0
    hit_rate: Optional[float] = None
    average_signal_score: Optional[float] = None
    average_edge_snapshot: Optional[float] = None

    action_class_distribution: Dict[str, int] = Field(default_factory=dict)
    market_distribution: Dict[str, int] = Field(default_factory=dict)
    policy_distribution: Dict[str, int] = Field(default_factory=dict)

    replay_log_loss: Optional[float] = None
    replay_brier: Optional[float] = None
    average_final_probability: Optional[float] = None


class BacktestRunManifest(BaseModel):
    run_id: str
    generated_at_utc: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str
    execution_policy_name: str
    window: ReplayWindowDefinition

    summary: BacktestSummaryRecord
    action_subsets: List[ActionSubsetSummary] = Field(default_factory=list)
    period_summaries: List[BacktestPeriodSummary] = Field(default_factory=list)

    ledger_artifact_path: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
