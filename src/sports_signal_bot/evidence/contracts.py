from datetime import datetime
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field

class CitationTrailRecord(BaseModel):
    citation_id: str
    citation_type: str
    source_family: str
    source_ref: str
    artifact_ref: str
    manifest_ref: str
    field_path: Optional[str] = None
    record_key: Optional[str] = None
    snapshot_time: Optional[datetime] = None
    notes: str

class EvidenceClaimRecord(BaseModel):
    claim_id: str
    claim_type: str
    claim_text: str
    claim_status: Literal["supported", "weakly_supported", "partially_supported", "contradicted", "unresolved", "informational"]
    support_strength: Literal["high", "medium", "low", "disputed", "unknown"]
    evidence_refs: List[str] = Field(default_factory=list)
    citation_refs: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    confidence_score: float

class EvidenceLineageNode(BaseModel):
    node_id: str
    node_type: str
    payload_summary: Dict[str, Any]
    schema_version: str

class EvidenceLineageEdge(BaseModel):
    source_node_id: str
    target_node_id: str
    relation_type: str

class EvidenceGraphRecord(BaseModel):
    graph_id: str
    nodes: List[EvidenceLineageNode]
    edges: List[EvidenceLineageEdge]

class ExplanationWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class EvidenceBundleRecord(BaseModel):
    bundle_id: str
    bundle_type: str
    target_entity_type: str
    target_entity_id: str
    sport: Optional[str] = None
    market_type: Optional[str] = None
    audience_profile: str
    evidence_status: str
    confidence_band: str
    claims: List[EvidenceClaimRecord] = Field(default_factory=list)
    citations: List[CitationTrailRecord] = Field(default_factory=list)
    lineage_refs: List[str] = Field(default_factory=list)
    warnings: List[ExplanationWarningRecord] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class CounterfactualHintRecord(BaseModel):
    hint_id: str
    hint_text: str
    status: Literal["informative_only", "approximate", "not_for_execution"]
    parameters_changed: Dict[str, Any]
    expected_outcome: str

class ExplanationPacketRecord(BaseModel):
    packet_id: str
    packet_type: str
    target_id: str
    bundle: EvidenceBundleRecord
    summary: str
    why_text: str
    why_not_text: Optional[str] = None
    what_changed_text: Optional[str] = None
    counterfactuals: List[CounterfactualHintRecord] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class ExplanationManifest(BaseModel):
    manifest_id: str
    timestamp: datetime
    bundle_count_by_type: Dict[str, int]
    claims_by_status: Dict[str, int]
    low_confidence_bundle_count: int
    disputed_explanation_count: int
    missing_citation_count: int
    top_why_not_reasons: Dict[str, int]
    audience_profile_distribution: Dict[str, int]
