from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EndToEndValidationCorridorRecord(BaseModel):
    validation_corridor_id: str
    corridor_family: str
    stage_refs: List[str] = []
    checkpoint_refs: List[str] = []
    evidence_refs: List[str] = []
    gap_refs: List[str] = []
    residue_refs: List[str] = []
    rollback_refs: List[str] = []
    replay_refs: List[str] = []
    corridor_status: str
    warnings: List[str] = []

class ValidationCorridorStageRecord(BaseModel):
    stage_id: str
    stage_family: str
    status: str

class ValidationCorridorCheckpointRecord(BaseModel):
    checkpoint_id: str
    checkpoint_family: str

class ValidationCorridorEvidenceRecord(BaseModel):
    evidence_id: str

class ValidationCorridorGapRecord(BaseModel):
    gap_id: str

class ValidationCorridorResidueRecord(BaseModel):
    residue_id: str

class ValidationCorridorRollbackRecord(BaseModel):
    rollback_id: str

class ValidationCorridorReplayRecord(BaseModel):
    replay_id: str

class EndToEndValidationHealthRecord(BaseModel):
    is_healthy: bool
    status: str

class EndToEndValidationManifestRecord(BaseModel):
    manifest_id: str

class EndToEndValidationWarningRecord(BaseModel):
    warning: str

class ReleaseGatingMeshRecord(BaseModel):
    release_gating_mesh_id: str
    mesh_family: str
    node_refs: List[str] = []
    edge_refs: List[str] = []
    gate_refs: List[str] = []
    blocker_refs: List[str] = []
    cap_refs: List[str] = []
    residue_refs: List[str] = []
    decision_refs: List[str] = []
    mesh_status: str
    warnings: List[str] = []

class GatingMeshNodeRecord(BaseModel):
    node_id: str

class GatingMeshEdgeRecord(BaseModel):
    edge_id: str

class GatingMeshGateRecord(BaseModel):
    gate_id: str

class GatingMeshBlockerRecord(BaseModel):
    blocker_id: str

class GatingMeshCapRecord(BaseModel):
    cap_id: str

class GatingMeshResidueRecord(BaseModel):
    residue_id: str

class GatingMeshDecisionRecord(BaseModel):
    decision_id: str

class ReleaseGatingMeshHealthRecord(BaseModel):
    is_healthy: bool

class ReleaseGatingMeshManifestRecord(BaseModel):
    manifest_id: str

class ReleaseGatingMeshWarningRecord(BaseModel):
    warning: str

class OperatorProofPackRecord(BaseModel):
    operator_proof_pack_id: str
    pack_family: str
    section_refs: List[str] = []
    evidence_refs: List[str] = []
    replay_refs: List[str] = []
    gap_refs: List[str] = []
    residue_refs: List[str] = []
    rollback_refs: List[str] = []
    continuity_refs: List[str] = []
    pack_status: str
    warnings: List[str] = []

class ProofPackSectionRecord(BaseModel):
    section_id: str

class ProofPackEvidenceRecord(BaseModel):
    evidence_id: str

class ProofPackReplayRecord(BaseModel):
    replay_id: str

class ProofPackResidueRecord(BaseModel):
    residue_id: str

class ProofPackGapRecord(BaseModel):
    gap_id: str

class ProofPackRollbackRecord(BaseModel):
    rollback_id: str

class ProofPackContinuityRecord(BaseModel):
    continuity_id: str

class OperatorProofPackHealthRecord(BaseModel):
    is_healthy: bool

class OperatorProofPackManifestRecord(BaseModel):
    manifest_id: str

class OperatorProofPackWarningRecord(BaseModel):
    warning: str

class ReplayClosureCompilerRecord(BaseModel):
    replay_closure_compiler_id: str
    compiler_family: str
    input_refs: List[str] = []
    pass_refs: List[str] = []
    gap_refs: List[str] = []
    residue_refs: List[str] = []
    decision_refs: List[str] = []
    drift_refs: List[str] = []
    rollback_refs: List[str] = []
    compiler_status: str
    warnings: List[str] = []

class ReplayClosureInputRecord(BaseModel):
    input_id: str

class ReplayClosurePassRecord(BaseModel):
    pass_id: str

class ReplayClosureGapRecord(BaseModel):
    gap_id: str

class ReplayClosureResidueRecord(BaseModel):
    residue_id: str

class ReplayClosureDecisionRecord(BaseModel):
    decision_id: str

class ReplayClosureDriftRecord(BaseModel):
    drift_id: str

class ReplayClosureRollbackRecord(BaseModel):
    rollback_id: str

class ReplayClosureHealthRecord(BaseModel):
    is_healthy: bool

class ReplayClosureManifestRecord(BaseModel):
    manifest_id: str

class ReplayClosureWarningRecord(BaseModel):
    warning: str
