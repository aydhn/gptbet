
from datetime import datetime
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field

class SourceObservationRecord(BaseModel):
    source_observation_id: str
    provider_name: str
    provider_kind: str
    data_family: str
    sport: str
    entity_type: str
    entity_key: str
    event_id: Optional[str] = None
    payload: Dict[str, Any]
    source_snapshot_time: datetime
    fetched_at: datetime
    provider_quality_score: float
    provider_health_status: str
    lineage_ref: str
    warnings: List[str] = Field(default_factory=list)

class ReconciliationGroupRecord(BaseModel):
    group_id: str
    data_family: str
    sport: str
    entity_key: str
    source_count: int
    providers_involved: List[str]
    reconciliation_status: str
    conflict_count: int
    confidence_score: float
    selected_consensus_strategy: str
    warnings: List[str] = Field(default_factory=list)
    observations: List[SourceObservationRecord] = Field(default_factory=list)

class FieldConflictRecord(BaseModel):
    conflict_id: str
    group_id: str
    field_name: str
    severity: Literal["low", "medium", "high", "critical"]
    conflict_type: str
    values: Dict[str, Any]
    resolved: bool = False

class ConflictClusterRecord(BaseModel):
    cluster_id: str
    group_id: str
    conflicts: List[FieldConflictRecord]

class ArbitrationDecisionRecord(BaseModel):
    decision_id: str
    group_id: str
    field_name: str
    selected_value: Any
    selected_source: Optional[str]
    strategy_used: str
    confidence: float
    disputed: bool

class ConsensusRecord(BaseModel):
    group_id: str
    entity_key: str
    data_family: str
    payload: Dict[str, Any]
    confidence_score: float
    disputed: bool

class TrustedUnifiedRecord(BaseModel):
    entity_key: str
    data_family: str
    trusted_payload: Dict[str, Any]
    field_resolution_map: Dict[str, str]
    selected_source_refs: List[str]
    consensus_strategy: str
    confidence_score: float
    dispute_flags: List[str]
    lineage: Dict[str, Any]
    warnings: List[str]

class ArbitrationConfidenceRecord(BaseModel):
    confidence_score: float
    confidence_band: Literal["high_confidence", "medium_confidence", "low_confidence", "disputed", "unresolved"]
    factors: Dict[str, float]

class SourceTrustAdjustmentRecord(BaseModel):
    provider_name: str
    data_family: str
    adjustment: float
    reason: str
    timestamp: datetime

class DisputeRecord(BaseModel):
    dispute_id: str
    group_id: str
    data_family: str
    entity_key: str
    reasons: List[str]
    severity: str
    status: str = "open"

class ReconciliationSummaryRecord(BaseModel):
    reconciled_group_count: int
    conflict_count: int
    dispute_count: int
    confidence_distribution: Dict[str, int]
    provider_disagreement_burden: Dict[str, int]
    auto_resolved_ratio: float

class ConsensusLineageRecord(BaseModel):
    field_name: str
    candidate_sources: List[str]
    candidate_values: List[Any]
    selected_value: Any
    strategy_used: str
    trust_scores: Dict[str, float]
    decision_explanation: str

class FieldResolutionRecord(BaseModel):
    field_name: str
    strategy: str
    resolved_value: Any

class ArbitrationWarningRecord(BaseModel):
    warning_id: str
    group_id: str
    message: str
    severity: str

class ReconciliationManifest(BaseModel):
    manifest_id: str
    timestamp: datetime
    sport: str
    data_family: str
    mode: str
    summary: ReconciliationSummaryRecord
    groups: List[ReconciliationGroupRecord]
    unified_records: List[TrustedUnifiedRecord]
    disputes: List[DisputeRecord]



class DisputeResolutionCandidate(BaseModel):
    dispute_id: str
    proposed_resolution: Any
    confidence_score: float

class ArbitrationReviewQueueRecord(BaseModel):
    queue_id: str
    dispute: DisputeRecord
    status: str = "pending"

class SourceTrustProfileRecord(BaseModel):
    provider_name: str
    data_family: str
    base_trust_score: float
    historical_accuracy: float
    penalty_multiplier: float

class ConsensusConfidenceModel(BaseModel):
    base_confidence: float
    conflict_penalties: float
    final_score: float
    band: str
