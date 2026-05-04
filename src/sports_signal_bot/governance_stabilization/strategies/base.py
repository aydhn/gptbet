from abc import ABC, abstractmethod
from typing import List, Optional
from ..contracts import (
    RecoveryQuorumMeshRecord,
    SuccessorFederationCouncilRecord,
    ExceptionLineageRegistryRecord,
    SovereignGovernanceStabilizationProgramRecord,
    RecoveryPathOutcome,
    SuccessorConvergenceBand,
    StabilizationDecision
)

class BaseStabilizationStrategy(ABC):
    @abstractmethod
    def evaluate_mesh_path(self, mesh: RecoveryQuorumMeshRecord) -> RecoveryPathOutcome:
        pass

    @abstractmethod
    def compute_successor_convergence(self, council: SuccessorFederationCouncilRecord) -> SuccessorConvergenceBand:
        pass

    @abstractmethod
    def evaluate_stabilization_stage(self, program: SovereignGovernanceStabilizationProgramRecord) -> StabilizationDecision:
        pass
