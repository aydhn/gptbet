import typer
import json
from .governance_stabilization.contracts import *
from .governance_stabilization.controllers import GovernanceStabilizationController
from .governance_stabilization.recovery_meshes import build_recovery_quorum_mesh, add_recovery_mesh_node, add_recovery_mesh_edge
from .governance_stabilization.successor_councils import build_successor_federation_council, open_successor_federation_case
from .governance_stabilization.lineage_registries import build_exception_lineage_registry, register_exception_lineage_entry
from .governance_stabilization.stabilization_programs import build_governance_stabilization_program, create_stabilization_checkpoint

app = typer.Typer(help="Phase 87: Sovereign Governance Stabilization CLI")

@app.command("run-governance-stabilization-pass")
def run_governance_stabilization_pass(sovereignty_deny: bool = typer.Option(False, help="Simulate a local sovereignty deny")):
    typer.echo("Running Governance Stabilization Pass...")

    ctrl = GovernanceStabilizationController()

    # Simulate a Mesh
    mesh = build_recovery_quorum_mesh("mesh_01", RecoveryMeshFamily.bounded_recovery_mesh)
    add_recovery_mesh_edge(mesh, RecoveryMeshEdgeRecord(
        edge_id="e1", source_node_ref="n1", target_node_ref="n2", edge_status=RecoveryEdgeStatus.edge_degraded
    ))
    ctrl.meshes.append(mesh)

    # Simulate a Council
    council = build_successor_federation_council("council_01", SuccessorCouncilFamily.federated_successor_currentness_council)
    open_successor_federation_case(council, "case_01", SuccessorCaseFamily.missing_successor_visibility_case)
    ctrl.councils.append(council)

    # Simulate Lineage
    registry = build_exception_lineage_registry("reg_01", ExceptionLineageRegistryFamily.sovereign_exception_lineage_registry)
    register_exception_lineage_entry(registry, ExceptionLineageEntryRecord(
        lineage_entry_id="entry_01", exception_ref="exc_1", status=ExceptionLineageEntryStatus.lineage_expired
    ))
    ctrl.registries.append(registry)

    # Simulate Program
    prog = build_governance_stabilization_program("prog_01", StabilizationProgramFamily.quorum_stabilization_program)
    create_stabilization_checkpoint(prog, "cp_01", StabilizationCheckpointFamily.sovereignty_constraints_preserved_checkpoint)
    ctrl.programs.append(prog)

    # Run pass
    manifest = ctrl.run_stabilization_pass(local_deny_present=sovereignty_deny)

    # Write artifact
    with open("governance_stabilization_manifest.json", "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    typer.secho(f"Pass complete. System Health: {manifest.system_health}", fg=typer.colors.GREEN)
    typer.secho(f"Stabilization Programs Status: {manifest.stabilization_programs[0].current_stage.value}", fg=typer.colors.CYAN)
    typer.secho("Manifest saved to governance_stabilization_manifest.json")

@app.command("preview-recovery-quorum-meshes")
def preview_recovery_quorum_meshes():
    typer.echo("Previewing Recovery Quorum Meshes...")
    typer.echo("- mesh_01 (bounded_recovery_mesh): Pressure HIGH, Outcome capped to caveated_bounded_recovery_hint")

@app.command("preview-successor-councils")
def preview_successor_councils():
    typer.echo("Previewing Successor Councils...")
    typer.echo("- council_01: weak_convergence detected due to unresolved lineage. Hint downgraded to review_only.")

if __name__ == "__main__":
    app()
