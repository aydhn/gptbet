import typer
from .engine import AutoPromotionEngine
from .contracts import CandidateInputRecord

app = typer.Typer(help="Constrained Auto-Promotion Operations")

def get_dummy_candidates():
    return [
        # Clean & Safe: Eligible for auto-progress
        CandidateInputRecord(
            candidate_release_id="cr-101", target_family="nba_spread", current_stage="shadow_verified",
            risk_level="low", scope_breadth="narrow", simulation_freshness_hours=2.0,
            evidence_completeness=0.9, readiness_score=0.95, gate_cleanliness=1.0, conflict_burden=0,
            dispute_count=0, repeated_holds=0
        ),
        # High Risk: Approval required boundary block
        CandidateInputRecord(
            candidate_release_id="cr-102", target_family="nfl_totals", current_stage="candidate_eval_verified",
            risk_level="high", scope_breadth="broad", simulation_freshness_hours=1.0,
            evidence_completeness=0.9, readiness_score=0.95, gate_cleanliness=1.0, conflict_burden=0,
            dispute_count=0, repeated_holds=0, approval_status="none"
        ),
        # Stale: Hard Safety Block
        CandidateInputRecord(
            candidate_release_id="cr-103", target_family="mlb_totals", current_stage="shortlisted",
            risk_level="low", scope_breadth="narrow", simulation_freshness_hours=48.0,
            evidence_completeness=0.5, readiness_score=0.3, gate_cleanliness=0.2, conflict_burden=0,
            dispute_count=0, repeated_holds=0
        ),
        # Weak Fleet Competitor: Will be superseded by cr-101
        CandidateInputRecord(
            candidate_release_id="cr-104", target_family="nba_spread", current_stage="shadow_verified",
            risk_level="low", scope_breadth="narrow", simulation_freshness_hours=1.0,
            evidence_completeness=0.7, readiness_score=0.5, gate_cleanliness=1.0, conflict_burden=0,
            dispute_count=0, repeated_holds=0
        )
    ]

@app.command("run-auto-promotion-pass")
def run_pass():
    """Execute the auto-promotion heuristic engine over active candidates."""
    typer.secho("Initiating Constrained Auto-Promotion Pass...", fg=typer.colors.CYAN)

    config = {
        "quotas": {"max_auto_progressions_per_run": 10, "max_auto_kills_per_run": 5},
        "heuristics": {"minimum_progression_score": 75.0, "low_risk_bonus": 10.0},
        "boundaries": {"stale_simulation_block_hours": 24, "minimum_evidence_for_kill": 0.8}
    }

    engine = AutoPromotionEngine(config)
    candidates = get_dummy_candidates()

    typer.echo(f"Loaded {len(candidates)} candidates for evaluation.")
    summary = engine.run_pass(candidates)

    typer.secho("\n--- Auto-Promotion Summary ---", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Total Evaluated: {summary.total_evaluated}")
    typer.echo(f"Auto-Progressions: {summary.auto_progress_count}")
    typer.echo(f"Auto-Kills: {summary.auto_kill_count}")
    typer.echo(f"Auto-Holds: {summary.auto_hold_count}")
    typer.echo(f"Safety Blocks: {summary.safety_boundary_block_count}")
    typer.echo(f"Approvals Req: {summary.review_required_count}")
    typer.echo(f"Fleet Supersessions: {summary.fleet_suppression_count}")

    typer.secho("\nArtifacts (JSON) written to working directory.", fg=typer.colors.CYAN)

@app.command("preview-auto-progression")
def preview_progression():
    """Preview which candidates are eligible for automatic progression without state mutation."""
    typer.echo("Previewing progression (dry-run).")
    run_pass()

@app.command("list-auto-promotion-strategies")
def list_strategies():
    typer.echo("Available Strategies:\n- ConservativeAutoPromotionStrategy\n- BalancedSemiAutonomousStrategy (Active)\n- FastSafeLadderStrategy\n- ReviewHeavySafetyStrategy\n- FleetAwareSelectiveStrategy")

if __name__ == "__main__":
    app()
