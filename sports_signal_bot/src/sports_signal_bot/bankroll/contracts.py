import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class MissingOddsPolicy(str, Enum):
    SKIP = "skip"
    PROXY = "proxy"
    FAIL = "fail"

class OverlayStrategyName(str, Enum):
    FLAT_STAKE = "flat_stake"
    FIXED_FRACTION = "fixed_fraction"
    TIERED_FLAT = "tiered_flat"
    CONSERVATIVE_CAPPED_FRACTION = "conservative_capped_fraction"
    NO_FINANCIAL_SHADOW = "no_financial_shadow"
    ADVANCED_SIZING = "advanced_sizing"

class BankrollConfig(BaseModel):
    initial_bankroll: float = Field(default=10000.0, ge=0.0)
    default_overlay_strategy: OverlayStrategyName = OverlayStrategyName.FLAT_STAKE
    flat_stake_units: float = Field(default=100.0, ge=0.0)
    bankroll_fraction: float = Field(default=0.02, ge=0.0, le=1.0)
    min_stake_units: float = Field(default=10.0, ge=0.0)
    max_stake_units: float = Field(default=1000.0, ge=0.0)
    max_fraction_per_decision: float = Field(default=0.05, ge=0.0, le=1.0)
    round_stakes_to: Optional[float] = None
    missing_odds_policy: MissingOddsPolicy = MissingOddsPolicy.SKIP
    bankroll_floor: float = Field(default=0.0, ge=0.0)
    enable_no_financial_shadow: bool = False

class BankrollDecisionRecord(BaseModel):
    event_id: str
    market_type: str
    sport: str
    event_datetime_utc: datetime.datetime
    action_class: str
    executed_flag: bool
    signal_score: float = 0.0
    implied_odds: Optional[float] = None
    payout_multiple: Optional[float] = None
    result_status: str
    hit_flag: Optional[bool] = None

class DrawdownRecord(BaseModel):
    event_id: str
    timestamp: datetime.datetime
    drawdown_abs: float
    drawdown_pct: float
    is_new_trough: bool = False

class StreakRecord(BaseModel):
    event_id: str
    timestamp: datetime.datetime
    current_win_streak: int
    current_loss_streak: int
    is_new_win_record: bool = False
    is_new_loss_record: bool = False

class ExposureRecord(BaseModel):
    timestamp: datetime.datetime
    total_stake_outstanding: float = 0.0
    same_timestamp_batch_count: int = 1

class CapitalCurvePoint(BaseModel):
    timestamp: datetime.datetime
    bankroll: float
    pnl: float
    peak_to_date: float
    drawdown_abs: float
    drawdown_pct: float
    streak_state: StreakRecord
    exposure: Optional[ExposureRecord] = None

class BankrollLedgerRecord(BaseModel):
    event_id: str
    market_type: str
    sport: str
    event_datetime_utc: datetime.datetime
    action_class: str
    executed_flag: bool
    stake_units: float
    stake_fraction: Optional[float] = None
    bankroll_before: float
    bankroll_after: float
    pnl_units: float
    pnl_pct_bankroll: float
    cumulative_pnl_units: float
    cumulative_return_pct: float
    result_status: str
    hit_flag: Optional[bool] = None
    implied_odds: Optional[float] = None
    payout_multiple: Optional[float] = None
    overlay_strategy_name: str
    warnings: List[str] = Field(default_factory=list)
    run_id: str

class BankrollSummaryRecord(BaseModel):
    initial_bankroll: float
    ending_bankroll: float
    net_pnl_units: float
    return_pct: float
    avg_stake_units: float
    executed_count: int
    win_rate: float
    max_drawdown_pct: float
    longest_loss_streak: int
    longest_win_streak: int
    average_pnl_per_decision: float
    action_class_pnl_summary: Dict[str, float] = Field(default_factory=dict)
    by_market_pnl_summary: Dict[str, float] = Field(default_factory=dict)

class BankrollRunManifest(BaseModel):
    run_id: str
    timestamp: datetime.datetime
    sport: str
    market: str
    overlay_strategy: str
    config: BankrollConfig
    summary: BankrollSummaryRecord
    ledger_artifact_path: Optional[str] = None
    curve_artifact_path: Optional[str] = None
    drawdown_artifact_path: Optional[str] = None
    streak_artifact_path: Optional[str] = None
