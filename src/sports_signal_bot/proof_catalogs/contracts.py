import dataclasses
from typing import List, Optional, Dict

@dataclasses.dataclass
class EvidenceAtlasFederationRecord:
    atlas_federation_id: str
    federation_family: str
    member_atlas_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    lineage_policy_ref: str
    applicability_policy_ref: str
    health_status: str
    warnings: List[str]

@dataclasses.dataclass
class FederatedAtlasNodeRecord:
    node_id: str
    atlas_ref: str
    atlas_family: str
    supported_view_families: List[str]
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str]

@dataclasses.dataclass
class AtlasFederationLinkRecord:
    link_id: str
    source_node_ref: str
    target_node_ref: str
    link_status: str
    warnings: List[str]

@dataclasses.dataclass
class AtlasFederationCurrentnessRecord:
    currentness_id: str
    state: str

@dataclasses.dataclass
class AtlasFederationLineageRecord:
    lineage_id: str

@dataclasses.dataclass
class AtlasFederationApplicabilityRecord:
    applicability_id: str

@dataclasses.dataclass
class AtlasFederationCaveatRecord:
    caveat_id: str

@dataclasses.dataclass
class AtlasFederationDecisionRecord:
    decision_id: str

@dataclasses.dataclass
class AtlasFederationHealthRecord:
    health_id: str
    status: str

@dataclasses.dataclass
class EvidenceAtlasFederationManifestRecord:
    manifest_id: str
    federation_refs: List[str]

@dataclasses.dataclass
class EvidenceAtlasFederationWarningRecord:
    warning_id: str

@dataclasses.dataclass
class NarrativeAuditBoardRecord:
    narrative_audit_board_id: str
    board_family: str
    governed_narrative_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str]

@dataclasses.dataclass
class NarrativeAuditCaseRecord:
    narrative_audit_case_id: str
    case_family: str
    input_narrative_refs: List[str]
    input_dashboard_refs: List[str]
    input_atlas_refs: List[str]
    input_proof_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: str
    warnings: List[str]

@dataclasses.dataclass
class NarrativeAuditInputRecord:
    input_id: str

@dataclasses.dataclass
class NarrativeAuditEvidenceRecord:
    evidence_id: str

@dataclasses.dataclass
class NarrativeAuditVoteRecord:
    vote_id: str

@dataclasses.dataclass
class NarrativeAuditDecisionRecord:
    decision_id: str

@dataclasses.dataclass
class NarrativeAuditCapRecord:
    cap_id: str

@dataclasses.dataclass
class NarrativeAuditFindingRecord:
    finding_id: str

@dataclasses.dataclass
class NarrativeAuditBacklogRecord:
    backlog_id: str

@dataclasses.dataclass
class NarrativeAuditHealthRecord:
    health_id: str

@dataclasses.dataclass
class NarrativeAuditBoardManifestRecord:
    manifest_id: str
    board_refs: List[str]

@dataclasses.dataclass
class NarrativeAuditBoardWarningRecord:
    warning_id: str

@dataclasses.dataclass
class AssuranceMeshObservatoryRecord:
    observatory_id: str
    observatory_family: str
    monitored_mesh_refs: List[str]
    scope_refs: List[str]
    snapshot_refs: List[str]
    signal_refs: List[str]
    anomaly_refs: List[str]
    alert_refs: List[str]
    health_status: str
    warnings: List[str]

@dataclasses.dataclass
class ObservatoryScopeRecord:
    scope_id: str

@dataclasses.dataclass
class ObservatorySnapshotRecord:
    observatory_snapshot_id: str
    source_mesh_ref: str
    source_view_refs: List[str]
    currentness_state: str
    pressure_state: str
    anomaly_state: str
    degraded_path_refs: List[str]
    warnings: List[str]

@dataclasses.dataclass
class ObservatorySignalRecord:
    signal_id: str
    signal_type: str

@dataclasses.dataclass
class ObservatoryAnomalyRecord:
    anomaly_id: str
    anomaly_type: str

@dataclasses.dataclass
class ObservatoryDriftRecord:
    drift_id: str

@dataclasses.dataclass
class ObservatoryPanelRecord:
    panel_id: str

@dataclasses.dataclass
class ObservatoryAlertRecord:
    alert_id: str

@dataclasses.dataclass
class ObservatoryHealthRecord:
    health_id: str

@dataclasses.dataclass
class AssuranceMeshObservatoryManifestRecord:
    manifest_id: str
    observatory_refs: List[str]

@dataclasses.dataclass
class AssuranceMeshObservatoryWarningRecord:
    warning_id: str

@dataclasses.dataclass
class SovereignGovernanceProofCatalogRecord:
    proof_catalog_id: str
    catalog_family: str
    entry_refs: List[str]
    class_refs: List[str]
    lineage_refs: List[str]
    applicability_refs: List[str]
    verification_refs: List[str]
    health_status: str
    warnings: List[str]

@dataclasses.dataclass
class ProofCatalogEntryRecord:
    proof_entry_id: str
    proof_family: str
    source_ref: str
    source_family: str
    proof_class_ref: str
    currentness_state: str
    applicability_scope: str
    caveat_state: str
    warnings: List[str]

@dataclasses.dataclass
class ProofCatalogClassRecord:
    class_id: str

@dataclasses.dataclass
class ProofCatalogLineageRecord:
    lineage_id: str

@dataclasses.dataclass
class ProofCatalogApplicabilityRecord:
    applicability_id: str

@dataclasses.dataclass
class ProofCatalogFreshnessRecord:
    freshness_id: str

@dataclasses.dataclass
class ProofCatalogVerificationRecord:
    verification_id: str

@dataclasses.dataclass
class ProofCatalogQueryRecord:
    query_id: str

@dataclasses.dataclass
class ProofCatalogHealthRecord:
    health_id: str

@dataclasses.dataclass
class GovernanceProofCatalogManifestRecord:
    manifest_id: str
    catalog_refs: List[str]

@dataclasses.dataclass
class GovernanceProofCatalogWarningRecord:
    warning_id: str
