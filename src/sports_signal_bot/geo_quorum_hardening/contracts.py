from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class RegionalQuorumDrillRecord(BaseModel):
    quorum_drill_id: str
    drill_family: str
    region_refs: List[str]
    member_refs: List[str]
    window_refs: List[str]
    decision_refs: List[str]
    gap_refs: List[str]
    residue_refs: List[str]
    recovery_refs: List[str]
    quorum_status: Literal["quorum_verified", "quorum_caveated", "quorum_review_only", "quorum_gapped", "quorum_blocked", "quorum_overclaimed"]
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActivePassiveRehearsalRecord(BaseModel):
    active_passive_rehearsal_id: str
    rehearsal_family: str
    active_region_ref: str
    passive_region_ref: str
    readiness_refs: List[str]
    lag_refs: List[str]
    fallback_refs: List[str]
    residue_refs: List[str]
    rehearsal_status: Literal["rehearsal_honest", "rehearsal_caveated", "rehearsal_review_only", "rehearsal_gapped", "rehearsal_blocked", "rehearsal_overclaimed"]
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GlobalOperatorCoverageSynthesisRecord(BaseModel):
    coverage_synthesis_id: str
    synthesis_family: str
    region_refs: List[str]
    window_refs: List[str]
    owner_refs: List[str]
    seam_refs: List[str]
    overlap_refs: List[str]
    gap_refs: List[str]
    escalation_reachability_refs: List[str]
    synthesis_status: Literal["coverage_synthesized", "coverage_caveated", "coverage_review_only", "coverage_gapped", "coverage_blocked"]
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RollingEvacuationAuditChainRecord(BaseModel):
    evacuation_chain_id: str
    chain_family: str
    wave_refs: List[str]
    checkpoint_refs: List[str]
    dependency_refs: List[str]
    rollback_refs: List[str]
    residue_refs: List[str]
    gap_refs: List[str]
    continuity_refs: List[str]
    chain_status: Literal["chain_verified", "chain_caveated", "chain_review_only", "chain_gapped", "chain_broken", "chain_overclaimed"]
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GeoQuorumHardeningManifestRecord(BaseModel):
    manifest_id: str
    regional_quorum_drill_refs: List[str]
    active_passive_rehearsal_refs: List[str]
    global_coverage_synthesis_refs: List[str]
    rolling_evacuation_chain_refs: List[str]
    overall_status: Literal["healthy", "degraded", "blocked"]
    warnings: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
