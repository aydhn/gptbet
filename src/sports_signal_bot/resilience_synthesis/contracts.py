from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


# --- Health Compiler Federation Contracts ---

class CompilerFederationCurrentnessRecord(BaseModel):
    currentness_id: str
    evaluated_at: str
    staleness_level: Literal["fresh", "grace_period", "stale", "expired"]
    warnings: List[str] = Field(default_factory=list)

class CompilerFederationScopeRecord(BaseModel):
    scope_id: str
    scope_type: Literal["full_governance", "restricted_replay", "successor_only", "exception_only"]
    boundaries: List[str] = Field(default_factory=list)

class CompilerFederationPenaltyRecord(BaseModel):
    penalty_id: str
    penalty_type: Literal["stale_federation_penalty", "low_consensus_penalty", "divergent_output_penalty"]
    severity: Literal["low", "moderate", "high", "critical"]
    description: str

class CompilerFederationCeilingRecord(BaseModel):
    ceiling_id: str
    max_band: Literal["review_only", "bounded_resilience_with_caveats", "stabilized_resilience_with_caps", "strong_bounded_resilience"]
    reason: str

class CompilerFederationDecisionRecord(BaseModel):
    decision_id: str
    federated_outcome: Literal["aggregated_review_only_health", "aggregated_bounded_health_with_caveats", "aggregated_stabilized_with_caps", "aggregated_fragile_health", "aggregated_blocked", "aggregated_no_safe_preserved"]
    rationale: str

class CompilerFederationHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status: Literal["healthy", "degraded", "failing", "blocked"]
    warnings: List[str] = Field(default_factory=list)

class FederatedCompilerNodeRecord(BaseModel):
    node_id: str
    compiler_ref: str
    compiler_family: str
    supported_scope_refs: List[str] = Field(default_factory=list)
    currentness_state: CompilerFederationCurrentnessRecord
    replay_state: str
    debt_state: str
    node_status: Literal["active", "failing", "stale", "offline"]
    warnings: List[str] = Field(default_factory=list)

class CompilerFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    link_status: Literal["link_current", "link_caveated", "link_review_only", "link_degraded", "link_backpressured", "link_blocked", "link_expired", "link_superseded"]

class HealthCompilerFederationRecord(BaseModel):
    compiler_federation_id: str
    federation_family: Literal[
        "stabilization_health_compiler_federation",
        "replay_health_compiler_federation",
        "successor_convergence_health_compiler_federation",
        "exception_burden_health_compiler_federation",
        "sovereignty_preservation_health_compiler_federation",
        "composite_governance_health_federation",
        "review_only_health_federation"
    ]
    member_compiler_refs: List[str] = Field(default_factory=list)
    federation_link_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    ceiling_policy_ref: str
    penalty_policy_ref: str
    health_status: CompilerFederationHealthRecord
    warnings: List[str] = Field(default_factory=list)

class HealthCompilerFederationWarningRecord(BaseModel):
    warning_id: str
    message: str

class HealthCompilerFederationManifestRecord(BaseModel):
    manifest_id: str
    federation_refs: List[str] = Field(default_factory=list)
    created_at: str


# --- Replay Workload Exchange Contracts ---

class ReplayExchangeScopeRecord(BaseModel):
    scope_id: str
    allowed_actions: List[str] = Field(default_factory=list)

class ReplayExchangeConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ReplayExchangeVerificationRecord(BaseModel):
    verification_id: str
    is_verified: bool
    evidence_found: bool

class ReplayExchangeRoutingRecord(BaseModel):
    routing_id: str
    route_outcome: Literal["routed_bounded_replay", "routed_review_only_replay", "routed_caveated_replay", "routed_degraded_replay", "routed_replay_required", "blocked_replay_route", "no_safe_replay_route"]
    selected_target_ref: Optional[str]

class ReplayExchangeReplayRecord(BaseModel):
    replay_id: str
    result: str

class ReplayExchangeHealthRecord(BaseModel):
    health_id: str
    status: Literal["healthy", "degraded", "failing"]

class ReplayExchangeEnvelopeRecord(BaseModel):
    envelope_id: str
    packet_ref: str
    routing_ref: str

class ReplayExchangePacketRecord(BaseModel):
    replay_exchange_packet_id: str
    workload_ref: str
    lineage_target_refs: List[str] = Field(default_factory=list)
    replay_family: str
    required_fidelity: str
    required_evidence_refs: List[str] = Field(default_factory=list)
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    currentness_refs: List[str] = Field(default_factory=list)
    scope_constraints: ReplayExchangeScopeRecord
    warnings: List[str] = Field(default_factory=list)

class ReplayWorkloadExchangeRecord(BaseModel):
    replay_exchange_id: str
    source_fabric_refs: List[str] = Field(default_factory=list)
    target_fabric_refs: List[str] = Field(default_factory=list)
    workload_packet_refs: List[str] = Field(default_factory=list)
    exchange_scope: ReplayExchangeScopeRecord
    validity_window: str
    evidence_refs: List[str] = Field(default_factory=list)
    replay_support_refs: List[str] = Field(default_factory=list)
    exchange_status: Literal["prepared", "validated", "exchanged_review_only", "exchanged_bounded", "exchanged_caveated", "exchanged_degraded", "exchanged_blocked", "exchanged_expired", "exchanged_superseded"]
    warnings: List[str] = Field(default_factory=list)

class ReplayWorkloadExchangeManifestRecord(BaseModel):
    manifest_id: str
    exchange_refs: List[str] = Field(default_factory=list)

class ReplayWorkloadExchangeWarningRecord(BaseModel):
    warning_id: str
    message: str


# --- Convergence Debt Ledger Contracts ---

class DebtOriginRecord(BaseModel):
    origin_id: str
    origin_type: str

class DebtAgeRecord(BaseModel):
    age_id: str
    days_old: int
    is_aging: bool

class DebtSeverityRecord(BaseModel):
    severity_id: str
    level: Literal["low", "moderate", "high", "critical", "structurally_blocking"]

class DebtSettlementCandidateRecord(BaseModel):
    candidate_id: str
    debt_ref: str
    settlement_strategy: str

class DebtSettlementDecisionRecord(BaseModel):
    decision_id: str
    is_settled: bool
    resolution_details: str

class DebtReplayLinkRecord(BaseModel):
    link_id: str
    replay_ref: str

class DebtLineageLinkRecord(BaseModel):
    link_id: str
    lineage_ref: str

class ConvergenceDebtHealthRecord(BaseModel):
    health_id: str
    status: Literal["healthy", "at_risk", "unhealthy"]

class ConvergenceDebtEntryRecord(BaseModel):
    debt_entry_id: str
    debt_family: Literal[
        "unresolved_successor_debt",
        "stale_successor_debt",
        "replay_divergence_debt",
        "lineage_fragment_debt",
        "applicability_conflict_debt",
        "successor_visibility_debt",
        "restoration_ceiling_debt",
        "no_safe_preservation_debt"
    ]
    source_successor_case_refs: List[str] = Field(default_factory=list)
    source_lineage_refs: List[str] = Field(default_factory=list)
    source_replay_refs: List[str] = Field(default_factory=list)
    debt_severity: DebtSeverityRecord
    debt_age: DebtAgeRecord
    debt_status: Literal["debt_open", "debt_caveated", "debt_review_only", "debt_aging", "debt_settlement_pending", "debt_settled", "debt_superseded", "debt_expired", "debt_blocked"]
    bounded_effect_summary: str
    warnings: List[str] = Field(default_factory=list)

class ConvergenceDebtLedgerRecord(BaseModel):
    convergence_debt_ledger_id: str
    ledger_family: Literal[
        "sovereign_convergence_debt_ledger",
        "replay_sensitive_debt_ledger",
        "successor_visibility_debt_ledger",
        "lineage_fragment_debt_ledger",
        "applicability_conflict_debt_ledger",
        "stabilization_burden_debt_ledger",
        "review_only_debt_ledger"
    ]
    tracked_debt_refs: List[str] = Field(default_factory=list)
    active_debt_entry_refs: List[str] = Field(default_factory=list)
    settled_debt_entry_refs: List[str] = Field(default_factory=list)
    replay_link_refs: List[str] = Field(default_factory=list)
    lineage_link_refs: List[str] = Field(default_factory=list)
    health_status: ConvergenceDebtHealthRecord
    warnings: List[str] = Field(default_factory=list)

class ConvergenceDebtLedgerManifestRecord(BaseModel):
    manifest_id: str
    ledger_refs: List[str] = Field(default_factory=list)

class ConvergenceDebtLedgerWarningRecord(BaseModel):
    warning_id: str
    message: str


# --- Sovereign Governance Resilience Score Synthesis Contracts ---

class SynthesisInputRecord(BaseModel):
    synthesis_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    replay_state: str
    convergence_state: str
    debt_state: str
    warnings: List[str] = Field(default_factory=list)

class SynthesisPassRecord(BaseModel):
    pass_id: str
    pass_type: Literal[
        "federated_currentness_pass",
        "replay_stability_pass",
        "convergence_quality_pass",
        "debt_burden_pass",
        "lineage_integrity_pass",
        "sovereignty_preservation_pass",
        "restoration_ceiling_pass",
        "no_safe_visibility_pass",
        "compiler_federation_pass"
    ]
    is_successful: bool
    notes: str

class SynthesisDimensionRecord(BaseModel):
    dimension_id: str
    dimension_type: Literal[
        "federated_health_quality",
        "replay_support_quality",
        "convergence_quality",
        "debt_hygiene",
        "lineage_integrity",
        "exception_pressure",
        "restoration_ceiling",
        "sovereignty_preservation",
        "no_safe_visibility_integrity",
        "stabilization_portfolio_balance",
        "replay_backlog_pressure",
        "successor_resolution_progress"
    ]
    score: float

class SynthesisPenaltyRecord(BaseModel):
    penalty_id: str
    penalty_family: Literal[
        "stale_federation_penalty",
        "replay_backlog_penalty",
        "replay_mismatch_penalty",
        "unresolved_successor_penalty",
        "lineage_gap_penalty",
        "debt_age_penalty",
        "exception_pressure_penalty",
        "sovereignty_suppression_penalty",
        "restoration_overclaim_penalty",
        "no_safe_visibility_penalty"
    ]
    impact: str

class SynthesisCeilingRecord(BaseModel):
    ceiling_id: str
    max_band: str
    reason: str

class SynthesisOutputRecord(BaseModel):
    output_id: str
    band: Literal["critically_fragile", "fragile", "review_only_resilience", "bounded_resilience_with_caveats", "stabilized_resilience_with_caps", "strong_bounded_resilience"]
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    no_safe_recovery_hint_preserved: bool

class SynthesisExplanationRecord(BaseModel):
    explanation_id: str
    details: str

class SynthesisHealthRecord(BaseModel):
    health_id: str
    status: str

class GovernanceResilienceScoreSynthesisRecord(BaseModel):
    synthesis_id: str
    synthesis_family: Literal[
        "federated_governance_resilience_synthesis",
        "replay_weighted_resilience_synthesis",
        "successor_weighted_resilience_synthesis",
        "debt_weighted_resilience_synthesis",
        "sovereignty_preserving_resilience_synthesis",
        "no_safe_visibility_resilience_synthesis",
        "composite_resilience_synthesis"
    ]
    input_refs: List[str] = Field(default_factory=list)
    pass_refs: List[str] = Field(default_factory=list)
    dimension_refs: List[str] = Field(default_factory=list)
    penalty_refs: List[str] = Field(default_factory=list)
    ceiling_refs: List[str] = Field(default_factory=list)
    output_refs: List[str] = Field(default_factory=list)
    current_state: str
    warnings: List[str] = Field(default_factory=list)

class GovernanceResilienceScoreManifestRecord(BaseModel):
    manifest_id: str
    synthesis_refs: List[str] = Field(default_factory=list)

class GovernanceResilienceScoreWarningRecord(BaseModel):
    warning_id: str
    message: str
