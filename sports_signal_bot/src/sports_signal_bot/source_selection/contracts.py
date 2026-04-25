from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class SourceExclusionReasonRecord(BaseModel):
    """Standardized reasons for excluding a source."""
    reason_code: str  # e.g., source_unavailable, stale_model, low_trust_score
    details: str

class SourceTrustScoreRecord(BaseModel):
    """Detailed breakdown of a source's trust score."""
    performance_score: float = 0.0
    recency_score: float = 0.0
    coverage_score: float = 0.0
    regime_fit_score: float = 0.0
    data_quality_score: float = 0.0
    disagreement_penalty: float = 0.0

    total_trust_score: float = Field(0.0, ge=0.0, le=1.0)
    component_breakdown: Dict[str, float] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)

class SourceEligibilityRecord(BaseModel):
    """Record representing the eligibility evaluation of a single source for an event."""
    event_id: str
    sport: str
    market_type: str
    source_name: str
    source_family: str

    is_available: bool = False
    is_eligible: bool = False

    eligibility_score: float = 0.0
    trust_score: Optional[SourceTrustScoreRecord] = None

    exclusion_reasons: List[SourceExclusionReasonRecord] = Field(default_factory=list)
    supporting_signals: Dict[str, Any] = Field(default_factory=dict)
    policy_name: str = "default"
    warnings: List[str] = Field(default_factory=list)

class SourceSelectionDecision(BaseModel):
    """Final decision regarding a candidate source."""
    source_name: str
    is_selected: bool
    reasoning: str
    eligibility_record: SourceEligibilityRecord

class SourceEligibilitySummary(BaseModel):
    """Summary statistics of the source selection process."""
    total_candidates: int = 0
    eligible_count: int = 0
    excluded_count: int = 0
    top_exclusion_reasons: Dict[str, int] = Field(default_factory=dict)
    family_eligibility_rates: Dict[str, float] = Field(default_factory=dict)
    stale_source_warnings: int = 0
    fallback_used: bool = False

class SourceSelectionDiagnostics(BaseModel):
    """Diagnostic information for debugging source selection."""
    regime_aware_notes: List[str] = Field(default_factory=list)
    fallback_decisions: List[str] = Field(default_factory=list)
    trust_score_distribution: Dict[str, float] = Field(default_factory=dict)
    execution_time_ms: float = 0.0

class SourceSelectionManifest(BaseModel):
    """Manifest of the entire source selection run."""
    run_id: str
    timestamp: str
    event_id: str
    sport: str
    market_type: str

    selected_sources: List[str]
    decisions: List[SourceSelectionDecision]
    summary: SourceEligibilitySummary
    diagnostics: SourceSelectionDiagnostics

class SourcePolicyDefinition(BaseModel):
    """Configuration for an eligibility policy."""
    policy_name: str
    is_enabled: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)
