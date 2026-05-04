import datetime
from .contracts import *
from .strategies.balanced_recovery_quorum import BalancedRecoveryQuorumStrategy
from .recovery_meshes import build_recovery_quorum_mesh, add_recovery_mesh_node, add_recovery_mesh_edge, compute_recovery_mesh_pressure
from .successor_councils import build_successor_federation_council, open_successor_federation_case, resolve_successor_federation_case
from .lineage_registries import build_exception_lineage_registry, register_exception_lineage_entry, detect_lineage_gaps
from .stabilization_programs import build_governance_stabilization_program, create_stabilization_checkpoint, verify_stabilization_checkpoints, advance_stabilization_program

class GovernanceStabilizationController:
    def __init__(self, strategy=None):
        self.strategy = strategy or BalancedRecoveryQuorumStrategy()
        self.meshes = []
        self.councils = []
        self.registries = []
        self.programs = []

    def enforce_sovereignty_across_phase87(self, local_deny_present: bool):
        """Rule: recovery quorum mesh local sovereignty deny’i asamaz"""
        if local_deny_present:
            for prog in self.programs:
                prog.decision = StabilizationDecision.mark_stabilization_blocked
                prog.current_stage = StabilizationStage.blocked_stabilization
                prog.warnings.append("Local sovereignty DENY overrides all stabilization efforts.")

    def run_stabilization_pass(self, local_deny_present: bool = False) -> GovernanceStabilizationManifestRecord:
        # 1. Evaluate Meshes & Pressure
        for mesh in self.meshes:
            compute_recovery_mesh_pressure(mesh)
            outcome = self.strategy.evaluate_mesh_path(mesh)
            mesh.paths.append(RecoveryMeshPathRecord(
                path_id=f"path_{mesh.recovery_mesh_id}",
                nodes=[n.node_id for n in mesh.node_refs],
                edges=[e.edge_id for e in mesh.edge_refs],
                outcome=outcome
            ))

        # 2. Evaluate Successor Councils
        for council in self.councils:
            convergence = self.strategy.compute_successor_convergence(council)
            for case in council.cases:
                if case.case_status == SuccessorCaseStatus.case_opened:
                    resolve_successor_federation_case(case, convergence, SuccessorCouncilDecision.downgrade_to_review_only_successor_hint)

        # 3. Evaluate Lineage
        for registry in self.registries:
            detect_lineage_gaps(registry)

        # 4. Advance Programs
        for prog in self.programs:
            verify_stabilization_checkpoints(prog, local_deny_present)
            decision = self.strategy.evaluate_stabilization_stage(prog)
            prog.decision = decision
            if decision == StabilizationDecision.restore_caveated_bounded_hint:
                advance_stabilization_program(prog, StabilizationStage.stabilized)

        # Enforce hard stops
        self.enforce_sovereignty_across_phase87(local_deny_present)

        return GovernanceStabilizationManifestRecord(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            recovery_meshes=self.meshes,
            successor_councils=self.councils,
            lineage_registries=self.registries,
            stabilization_programs=self.programs,
            system_health="degraded" if local_deny_present else "nominal"
        )
