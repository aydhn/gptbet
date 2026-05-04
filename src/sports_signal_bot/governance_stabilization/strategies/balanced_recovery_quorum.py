from .base import BaseStabilizationStrategy
from ..contracts import *

class BalancedRecoveryQuorumStrategy(BaseStabilizationStrategy):
    def evaluate_mesh_path(self, mesh: RecoveryQuorumMeshRecord) -> RecoveryPathOutcome:
        if mesh.pressure and mesh.pressure.pressure_state in [RecoveryPressureState.critical, RecoveryPressureState.high]:
            return RecoveryPathOutcome.review_only_recovery_hint

        has_degraded = any(e.edge_status == RecoveryEdgeStatus.edge_degraded for e in mesh.edge_refs)
        if has_degraded:
            return RecoveryPathOutcome.caveated_bounded_recovery_hint

        return RecoveryPathOutcome.bounded_recovery_hint

    def compute_successor_convergence(self, council: SuccessorFederationCouncilRecord) -> SuccessorConvergenceBand:
        unresolved = [c for c in council.cases if c.case_status not in [SuccessorCaseStatus.case_decided, SuccessorCaseStatus.case_archived]]
        if len(unresolved) > 0:
            return SuccessorConvergenceBand.weak_convergence
        return SuccessorConvergenceBand.stable_convergence

    def evaluate_stabilization_stage(self, program: SovereignGovernanceStabilizationProgramRecord) -> StabilizationDecision:
        all_checkpoints_cleared = all(cp.is_cleared for cp in program.checkpoints)
        if program.current_stage == StabilizationStage.blocked_stabilization:
            return StabilizationDecision.mark_stabilization_blocked

        if all_checkpoints_cleared:
            return StabilizationDecision.restore_caveated_bounded_hint
        else:
            return StabilizationDecision.preserve_review_only_bias
