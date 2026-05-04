from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class PortfolioEntryRecord(BaseModel):
    portfolio_entry_id: str
    stabilization_program_ref: str
    portfolio_role: Literal[
        "primary_recovery_entry",
        "support_recovery_entry",
        "replay_heavy_entry",
        "successor_heavy_entry",
        "burden_reduction_entry",
        "review_only_entry",
        "regression_watch_entry"
    ]
    current_stage_ref: str
    burden_refs: List[str] = Field(default_factory=list)
    dependency_refs: List[str] = Field(default_factory=list)
    priority_band: Literal[
        "stabilization_critical",
        "successor_critical",
        "replay_critical",
        "burden_reduction_critical",
        "review_only_support",
        "regression_watch",
        "opportunistic_cleanup"
    ]
    portfolio_status: Literal[
        "portfolio_balanced",
        "portfolio_caution",
        "portfolio_backlogged",
        "portfolio_replay_heavy",
        "portfolio_successor_blocked",
        "portfolio_exception_heavy",
        "portfolio_degraded",
        "portfolio_review_bias",
        "portfolio_blocked"
    ]
    warnings: List[str] = Field(default_factory=list)


class StabilizationProgramPortfolioRecord(BaseModel):
    portfolio_id: str
    portfolio_family: Literal[
        "quorum_stabilization_portfolio",
        "successor_resolution_portfolio",
        "replay_rebuild_portfolio",
        "exception_burden_reduction_portfolio",
        "degraded_governance_portfolio",
        "sovereignty_preservation_portfolio",
        "mixed_recovery_portfolio"
    ]
    monitored_program_refs: List[str] = Field(default_factory=list)
    entry_refs: List[str] = Field(default_factory=list)
    priority_policy_ref: str
    burden_policy_ref: str
    dependency_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)


class ReplayFabricNodeRecord(BaseModel):
    node_id: str
    node_family: Literal[
        "replay_ingress_node",
        "lineage_validation_node",
        "successor_replay_node",
        "exception_replay_node",
        "stabilization_checkpoint_replay_node",
        "degraded_replay_fallback_node",
        "replay_health_observer_node"
    ]
    supported_lineage_families: List[str] = Field(default_factory=list)
    replay_capacity: int
    replay_load: int
    currentness_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)


class ReplayFabricChannelRecord(BaseModel):
    channel_id: str
    source_node_ref: str
    target_node_ref: str
    supported_replay_families: List[str] = Field(default_factory=list)
    supported_scope_classes: List[str] = Field(default_factory=list)
    caveat_transfer_policy: str
    replay_integrity_policy_ref: str
    channel_status: Literal[
        "active",
        "caveated",
        "review_only",
        "degraded",
        "backpressured",
        "blocked",
        "expired",
        "superseded"
    ]
    warnings: List[str] = Field(default_factory=list)


class ReplayFabricWorkloadRecord(BaseModel):
    workload_id: str
    lineage_target_ref: str
    replay_family: str
    required_fidelity: str
    required_evidence_refs: List[str] = Field(default_factory=list)
    workload_priority: str
    workload_status: Literal[
        "queued",
        "replaying",
        "replayed_matched",
        "replayed_caveated",
        "replayed_mismatched",
        "replay_blocked",
        "replay_expired"
    ]
    output_replay_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class LineageReplayFabricRecord(BaseModel):
    replay_fabric_id: str
    fabric_family: Literal[
        "exception_lineage_replay_fabric",
        "successor_chain_replay_fabric",
        "stabilization_replay_fabric",
        "audit_support_replay_fabric",
        "degraded_replay_fabric",
        "review_only_replay_fabric",
        "currentness_revalidation_fabric"
    ]
    node_refs: List[str] = Field(default_factory=list)
    channel_refs: List[str] = Field(default_factory=list)
    workload_refs: List[str] = Field(default_factory=list)
    replay_policy_ref: str
    pressure_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)


class ConvergenceRegistryEntryRecord(BaseModel):
    convergence_entry_id: str
    source_successor_case_ref: str
    source_baseline_refs: List[str] = Field(default_factory=list)
    candidate_successor_refs: List[str] = Field(default_factory=list)
    selected_successor_ref: Optional[str] = None
    convergence_band: Literal[
        "no_convergence",
        "weak_convergence",
        "bounded_convergence",
        "strong_convergence_with_caveats",
        "stable_convergence",
        "stale_convergence"
    ]
    currentness_state: str
    evidence_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class SuccessorConvergenceRegistryRecord(BaseModel):
    convergence_registry_id: str
    registry_family: Literal[
        "sovereign_successor_convergence_registry",
        "replay_sensitive_convergence_registry",
        "applicability_weighted_convergence_registry",
        "degraded_successor_convergence_registry",
        "review_only_convergence_registry",
        "stabilization_support_convergence_registry"
    ]
    tracked_successor_refs: List[str] = Field(default_factory=list)
    entry_refs: List[str] = Field(default_factory=list)
    trend_refs: List[str] = Field(default_factory=list)
    debt_refs: List[str] = Field(default_factory=list)
    replay_link_refs: List[str] = Field(default_factory=list)
    health_status: str
    warnings: List[str] = Field(default_factory=list)


class CompilerInputRecord(BaseModel):
    input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    replay_state: str
    lineage_state: str
    applicability_state: str
    warnings: List[str] = Field(default_factory=list)


class SovereignGovernanceHealthCompilerRecord(BaseModel):
    compiler_id: str
    compiler_family: Literal[
        "stabilization_portfolio_health_compiler",
        "replay_fabric_health_compiler",
        "successor_convergence_health_compiler",
        "exception_burden_health_compiler",
        "governance_surface_health_compiler",
        "sovereignty_preservation_health_compiler",
        "composite_governance_health_compiler"
    ]
    input_refs: List[str] = Field(default_factory=list)
    pass_refs: List[str] = Field(default_factory=list)
    dimension_refs: List[str] = Field(default_factory=list)
    penalty_refs: List[str] = Field(default_factory=list)
    output_refs: List[str] = Field(default_factory=list)
    current_state: str
    warnings: List[str] = Field(default_factory=list)

class CompilerPassRecord(BaseModel):
    pass_id: str
    pass_type: Literal[
        "currentness_pass",
        "replay_pass",
        "convergence_pass",
        "lineage_pass",
        "burden_pass",
        "sovereignty_pass",
        "restoration_ceiling_pass",
        "no_safe_visibility_pass"
    ]
    status: str
    warnings: List[str] = Field(default_factory=list)

class CompilerPenaltyRecord(BaseModel):
    penalty_id: str
    penalty_family: Literal[
        "stale_replay_penalty",
        "unresolved_successor_penalty",
        "lineage_gap_penalty",
        "exception_burden_penalty",
        "degraded_path_penalty",
        "sovereignty_suppression_penalty",
        "replay_mismatch_penalty",
        "restoration_overclaim_penalty",
        "no_safe_visibility_penalty"
    ]
    severity: str
    explanation: str

class CompilerOutputRecord(BaseModel):
    output_id: str
    compiler_ref: str
    health_band: Literal[
        "critically_fragile",
        "fragile",
        "review_only_health",
        "bounded_health_with_caveats",
        "stabilized_with_caps",
        "strong_bounded_health"
    ]
    blockers: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    restoration_ceiling: str
    warnings: List[str] = Field(default_factory=list)
