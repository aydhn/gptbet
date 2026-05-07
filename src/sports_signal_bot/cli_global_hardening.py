import typer
from rich.console import Console
from .global_hardening.contracts import (
    RegionalQuorumMeshRecord, QuorumMeshNodeRecord,
    PlanetaryCoverageSynthesisRecord, CoverageSeamRecord, CoverageGapRecord,
    GlobalContinuityDrillRecord, ContinuityPhaseRecord, ContinuityResidueRecord, ContinuityGapRecord,
    CrossRegionRecoveryGovernanceRecord, GovernanceGapRecord,
    GlobalResilienceBudgetsRecord, BudgetConsumptionRecord, GlobalQuorumBudgetRecord
)
from .global_hardening.quorum_meshes import build_regional_quorum_mesh, add_quorum_mesh_node
from .global_hardening.planetary_coverage import build_planetary_coverage_synthesis, detect_planetary_coverage_seams, verify_planetary_coverage_handoff
from .global_hardening.continuity_drills import build_global_continuity_drill, advance_global_continuity_phase, record_global_continuity_residue, detect_global_continuity_gaps
from .global_hardening.recovery_governance import build_cross_region_recovery_governance, detect_cross_region_governance_gaps
from .global_hardening.budgets import build_global_resilience_budgets, add_quorum_budget, measure_global_budget_consumption
from .global_hardening.integration import build_global_continuity_matrix, summarize_global_continuity_matrix, export_artifacts
import json

app = typer.Typer()
console = Console()

@app.command("run-hardening-pack-11")
def run_hardening_pack_11():
    console.print("[bold green]Running Post-100 Hardening Pack 11...[/bold green]")

    mesh = build_regional_quorum_mesh("mesh_01", "bounded_regional_quorum_mesh")
    add_quorum_mesh_node(mesh, QuorumMeshNodeRecord(node_id="n1", node_family="primary_region_node", region="us-east", status="healthy"))
    add_quorum_mesh_node(mesh, QuorumMeshNodeRecord(node_id="n2", node_family="primary_region_node", region="eu-west", status="stale"))

    cov = build_planetary_coverage_synthesis("synthesis_01", "global_follow_the_sun_synthesis")
    detect_planetary_coverage_seams(cov, [CoverageSeamRecord(seam_id="seam_1", status="missing_ack")])
    verify_planetary_coverage_handoff(cov, CoverageGapRecord(gap_id="gap_1", duration_minutes=15))

    drill = build_global_continuity_drill("drill_01", "global_quorum_loss_drill")
    advance_global_continuity_phase(drill, ContinuityPhaseRecord(phase_id="p1", phase_family="regional_state_verification_phase"))
    record_global_continuity_residue(drill, ContinuityResidueRecord(residue_id="res_1", description="unresolved local state"))

    gov = build_cross_region_recovery_governance("gov_01", "regional_recovery_governance")
    detect_cross_region_governance_gaps(gov, GovernanceGapRecord(gap_id="gap_1", description="ambiguous ownership chain"))

    budgets = build_global_resilience_budgets("budget_01")
    add_quorum_budget(budgets, GlobalQuorumBudgetRecord(budget_id="qb_1", limit=100))
    measure_global_budget_consumption(budgets, BudgetConsumptionRecord(consumption_id="c_1", amount=150))

    matrix = build_global_continuity_matrix([mesh], [cov], [drill], [gov], [budgets])
    summary = summarize_global_continuity_matrix(matrix)
    export_artifacts(matrix, summary)

    console.print("[bold cyan]Global Hardening Results:[/bold cyan]")
    console.print(f"Mesh Verified: {summary['mesh_verified_count']}")
    console.print(f"Coverage Verified: {summary['coverage_verified_count']}")
    console.print(f"Drill Honest: {summary['drill_honest_count']}")
    console.print(f"Governance Verified: {summary['governance_verified_count']}")
    console.print(f"Total Warnings: {summary['total_warnings']}")
    console.print(f"Release Blockers: {summary['release_blockers']}")
    console.print(f"Overall Health: {summary['overall_health']}")

@app.command("preview-regional-quorum-mesh-report")
def preview_mesh():
    console.print("Previewing Regional Quorum Mesh Report...")

@app.command("preview-planetary-coverage-report")
def preview_coverage():
    console.print("Previewing Planetary Coverage Report...")

@app.command("preview-global-continuity-drill-report")
def preview_drill():
    console.print("Previewing Global Continuity Drill Report...")

@app.command("preview-cross-region-governance-report")
def preview_governance():
    console.print("Previewing Cross Region Governance Report...")

@app.command("preview-global-hardening-health")
def preview_health():
    with open("global_hardening_health_report.json", "r") as f:
        data = json.load(f)
        console.print(data)

@app.command("list-global-hardening-strategies")
def list_strategies():
    console.print("1. ConservativeGlobalHardeningStrategy")
    console.print("2. BalancedGlobalReadinessStrategy")
    console.print("3. QuorumMeshFirstStrategy")
    console.print("4. GovernanceClarityFirstStrategy")

if __name__ == "__main__":
    app()
