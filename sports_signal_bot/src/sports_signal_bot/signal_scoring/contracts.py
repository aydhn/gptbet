from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SignalStatus(str, Enum):
    SCORED = "scored"
    WEAK_SIGNAL = "weak_signal"
    NO_MARKET_REFERENCE = "no_market_reference"
    UNSUPPORTED_MARKET = "unsupported_market"
    INSUFFICIENT_QUALITY = "insufficient_quality"
    PENDING = "pending"
    INVALID = "invalid"


class SignalComponentRecord(BaseModel):
    edge_estimate: float = 0.0
    confidence_score: float = 0.0
    uncertainty_penalty: float = 0.0
    disagreement_penalty: float = 0.0
    data_quality_penalty: float = 0.0
    source_health_penalty: float = 0.0
    regime_adjustment: float = 0.0

    metadata: Dict[str, Any] = Field(default_factory=dict)


class SignalCandidateRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str
    final_probability: float
    market_implied_probability: Optional[float] = None

    # Contextual features
    class_probabilities: Dict[str, float] = Field(default_factory=dict)
    market_odds_value_proxy: Optional[float] = None
    fair_odds: Optional[float] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class SignalScoreRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str

    final_probability: float
    market_implied_probability: Optional[float] = None

    components: SignalComponentRecord

    final_signal_score: float
    normalized_score: Optional[float] = None

    strategy_name: str
    status: SignalStatus = SignalStatus.PENDING

    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)


class SignalDiagnosticsRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str

    strategy_used: str

    top_class_gap: float = 0.0
    entropy: float = 0.0
    max_disagreement: float = 0.0
    missing_features_ratio: float = 0.0
    stale_components_ratio: float = 0.0

    regime_labels: List[str] = Field(default_factory=list)

    warnings: List[str] = Field(default_factory=list)


class SignalRankingRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str
    final_signal_score: float
    normalized_score: Optional[float] = None
    rank: int = 0
    tier: str = "unranked"
    status: SignalStatus = SignalStatus.PENDING

    # Tie-break metrics
    edge_estimate: float = 0.0
    confidence_score: float = 0.0
    uncertainty_penalty: float = 0.0


class SignalManifest(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str
    strategy_name: str

    total_processed: int = 0
    scored_count: int = 0
    weak_signal_count: int = 0
    no_market_reference_count: int = 0
    invalid_count: int = 0

    top_signals: List[SignalRankingRecord] = Field(default_factory=list)
    weakest_signals: List[SignalRankingRecord] = Field(default_factory=list)

    score_distribution: Dict[str, int] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class SignalPolicyInputRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str
    final_probability: float
    final_signal_score: float
    normalized_score: Optional[float] = None
    status: SignalStatus
    rank: Optional[int] = None
    edge_estimate: float = 0.0

    # A simplified structure designed to be easily consumed by policy/threshold engines
    components_summary: Dict[str, float] = Field(default_factory=dict)
