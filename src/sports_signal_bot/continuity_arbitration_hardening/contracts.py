import dataclasses
from typing import List, Dict, Optional
from datetime import datetime, timezone

@dataclasses.dataclass
class ContinuityArbitrationRailHealthRecord:
    status: str
    last_verified: datetime
    warnings: List[str]

@dataclasses.dataclass
class ContinuityArbitrationRailManifestRecord:
    manifest_id: str
    generated_at: datetime
    rail_count: int

@dataclasses.dataclass
class ContinuityArbitrationRailWarningRecord:
    warning_code: str
    message: str
    severity: str

@dataclasses.dataclass
class ContinuityArbitrationRailRecord:
    continuity_arbitration_rail_id: str
    rail_family: str
    case_refs: List[str]
    input_refs: List[str]
    evidence_refs: List[str]
    decision_refs: List[str]
    cap_refs: List[str]
    residue_refs: List[str]
    rail_status: str
    warnings: List[str]

@dataclasses.dataclass
class ArbitrationRailCaseRecord:
    case_id: str
    case_family: str
    created_at: datetime
    status: str

@dataclasses.dataclass
class ArbitrationRailInputRecord:
    input_id: str
    source_ref: str
    payload: Dict

@dataclasses.dataclass
class ArbitrationRailEvidenceRecord:
    evidence_id: str
    is_fresh: bool
    evidence_type: str

@dataclasses.dataclass
class ArbitrationRailDecisionRecord:
    decision_id: str
    outcome: str
    rationale: str

@dataclasses.dataclass
class ArbitrationRailCapRecord:
    cap_id: str
    cap_type: str
    limit: str

@dataclasses.dataclass
class ArbitrationRailPrecedenceRecord:
    precedence_id: str
    rule_applied: str

@dataclasses.dataclass
class ArbitrationRailResidueRecord:
    residue_id: str
    unresolved_scope: str
    severity: str

# Scheduler Recovery Fabric Contracts
@dataclasses.dataclass
class SchedulerRecoveryFabricHealthRecord:
    status: str
    last_verified: datetime
    warnings: List[str]

@dataclasses.dataclass
class SchedulerRecoveryFabricManifestRecord:
    manifest_id: str
    generated_at: datetime
    fabric_count: int

@dataclasses.dataclass
class SchedulerRecoveryFabricWarningRecord:
    warning_code: str
    message: str
    severity: str

@dataclasses.dataclass
class SchedulerRecoveryFabricRecord:
    scheduler_recovery_fabric_id: str
    fabric_family: str
    lane_refs: List[str]
    path_refs: List[str]
    packet_refs: List[str]
    retry_refs: List[str]
    rollback_refs: List[str]
    gap_refs: List[str]
    residue_refs: List[str]
    fabric_status: str
    warnings: List[str]

@dataclasses.dataclass
class RecoveryFabricLaneRecord:
    lane_id: str
    lane_family: str

@dataclasses.dataclass
class RecoveryFabricPathRecord:
    path_id: str
    nodes: List[str]

@dataclasses.dataclass
class RecoveryFabricPacketRecord:
    packet_id: str
    payload_hash: str
    is_stale: bool

@dataclasses.dataclass
class RecoveryFabricRetryRecord:
    retry_id: str
    attempt_count: int

@dataclasses.dataclass
class RecoveryFabricRollbackRecord:
    rollback_id: str
    rollback_ready: bool

@dataclasses.dataclass
class RecoveryFabricGapRecord:
    gap_id: str
    severity: str

@dataclasses.dataclass
class RecoveryFabricResidueRecord:
    residue_id: str
    description: str

# Archive Proof Mesh Contracts
@dataclasses.dataclass
class ArchiveProofMeshHealthRecord:
    status: str
    last_verified: datetime
    warnings: List[str]

@dataclasses.dataclass
class ArchiveProofMeshManifestRecord:
    manifest_id: str
    generated_at: datetime
    mesh_count: int

@dataclasses.dataclass
class ArchiveProofMeshWarningRecord:
    warning_code: str
    message: str
    severity: str

@dataclasses.dataclass
class ArchiveProofMeshRecord:
    archive_proof_mesh_id: str
    mesh_family: str
    node_refs: List[str]
    edge_refs: List[str]
    path_refs: List[str]
    hash_refs: List[str]
    lineage_refs: List[str]
    replay_refs: List[str]
    residue_refs: List[str]
    mesh_status: str
    warnings: List[str]

@dataclasses.dataclass
class ProofMeshNodeRecord:
    node_id: str
    node_family: str

@dataclasses.dataclass
class ProofMeshEdgeRecord:
    edge_id: str
    source_node: str
    target_node: str

@dataclasses.dataclass
class ProofMeshPathRecord:
    path_id: str
    edges: List[str]

@dataclasses.dataclass
class ProofMeshHashRecord:
    hash_id: str
    hash_value: str

@dataclasses.dataclass
class ProofMeshLineageRecord:
    lineage_id: str
    is_intact: bool

@dataclasses.dataclass
class ProofMeshReplayRecord:
    replay_id: str
    replay_successful: bool

@dataclasses.dataclass
class ProofMeshResidueRecord:
    residue_id: str
    severity: str

# Worldwide Visibility Ledger Contracts
@dataclasses.dataclass
class WorldwideVisibilityLedgerHealthRecord:
    status: str
    last_verified: datetime
    warnings: List[str]

@dataclasses.dataclass
class WorldwideVisibilityLedgerManifestRecord:
    manifest_id: str
    generated_at: datetime
    ledger_count: int

@dataclasses.dataclass
class WorldwideVisibilityLedgerWarningRecord:
    warning_code: str
    message: str
    severity: str

@dataclasses.dataclass
class WorldwideVisibilityLedgerRecord:
    worldwide_visibility_ledger_id: str
    ledger_family: str
    entry_refs: List[str]
    shift_refs: List[str]
    suppression_refs: List[str]
    restoration_refs: List[str]
    gap_refs: List[str]
    residue_refs: List[str]
    continuity_refs: List[str]
    ledger_status: str
    warnings: List[str]

@dataclasses.dataclass
class VisibilityLedgerEntryRecord:
    entry_id: str
    entry_family: str

@dataclasses.dataclass
class VisibilityLedgerShiftRecord:
    shift_id: str
    shift_family: str

@dataclasses.dataclass
class VisibilityLedgerSuppressionRecord:
    suppression_id: str
    reason: str

@dataclasses.dataclass
class VisibilityLedgerRestorationRecord:
    restoration_id: str
    lineage_preserved: bool

@dataclasses.dataclass
class VisibilityLedgerGapRecord:
    gap_id: str
    severity: str

@dataclasses.dataclass
class VisibilityLedgerResidueRecord:
    residue_id: str
    description: str

@dataclasses.dataclass
class VisibilityLedgerContinuityRecord:
    continuity_id: str
    status: str
