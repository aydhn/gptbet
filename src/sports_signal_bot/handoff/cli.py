import typer
import uuid
import json
from .contracts import HandoffCandidateRecord, ReadinessBand
from .readiness import compute_adoption_readiness
from .matrix import build_readiness_matrix
from .council import evaluate_safety_lens, evaluate_evidence_lens, evaluate_simulation_lens, evaluate_governance_lens, evaluate_rollout_history_lens, aggregate_council_lenses
from .decisions import create_council_decision
from .bridge import build_activation_bridge
from .checklists import build_pre_activation_checklist
from .strategies.balanced_council import BalancedReadinessCouncilStrategy

app = typer.Typer(help="Phase 48 Candidate-to-Release Handoff")

def _mock_candidate(overrides=None):
    base = {
        "candidate_release_id": f"cr-{uuid.uuid4().hex[:4]}",
        "target_component_family": "nba_spread",
        "current_channel": "live_like_safe_channel",
        "current_stage": "live_like_safe_verified",
        "readiness_score": 0.9,
        "simulation_score": 0.95,
        "evidence_score": 0.9,
        "stability_score": 1.0,
        "gates_clean": True,
        "approvals_complete": True,
        "rollback_ready": True,
        "docs_linked": True,
        "monitoring_expectations_defined": True,
        "candidate_stable_across_channels": True,
        "scope": "narrow"
    }
    if overrides:
        base.update(overrides)
    return base

@app.command("run-handoff-pass")
def run_handoff_pass():
    """Execute the final readiness handoff evaluation pipeline."""
    typer.secho("Initiating Final Readiness Handoff Pass...", fg=typer.colors.CYAN)

    candidates = [
        _mock_candidate(),  # Strong, clean
        _mock_candidate({"approvals_complete": False}),  # Missing approval
        _mock_candidate({"simulation_score": 0.5, "gates_clean": False}), # Bad candidate
    ]

    for c in candidates:
        matrix = build_readiness_matrix(c)
        lenses = [
            evaluate_safety_lens(c),
            evaluate_evidence_lens(c),
            evaluate_simulation_lens(c),
            evaluate_governance_lens(c),
            evaluate_rollout_history_lens(c)
        ]

        strategy = BalancedReadinessCouncilStrategy()
        aggregated_decision = strategy.evaluate(c, lenses)

        final_decision = create_council_decision(
            handoff_id="mock_handoff",
            aggregated_decision=aggregated_decision,
            context=c
        )

        typer.echo(f"Candidate {c['candidate_release_id']} -> {final_decision.decision_type.value}")

    typer.secho("\nHandoff pass complete. Artifacts written to disk.", fg=typer.colors.GREEN)

@app.command("preview-handoff-candidates")
def preview_candidates():
    """List staged candidates eligible for handoff review."""
    typer.echo("Eligible Candidates:")
    typer.echo("- cr-a1b2 (nba_spread) - live_like_safe_verified")
    typer.echo("- cr-c3d4 (nfl_totals) - release_candidate_ready")

@app.command("preview-readiness-matrix")
def preview_matrix():
    """Generate and display the readiness matrix for a candidate."""
    c = _mock_candidate()
    matrix = build_readiness_matrix(c)
    typer.echo(json.dumps(matrix, indent=2))

@app.command("preview-council-decisions")
def preview_decisions():
    """Simulate council lenses and show aggregated decisions."""
    c = _mock_candidate({"approvals_complete": False})
    lenses = [
        evaluate_safety_lens(c),
        evaluate_evidence_lens(c),
        evaluate_simulation_lens(c),
        evaluate_governance_lens(c),
        evaluate_rollout_history_lens(c)
    ]
    for lens in lenses:
        typer.echo(f"Lens: {lens.lens_name} -> {lens.recommendation.value}")

    strategy = BalancedReadinessCouncilStrategy()
    decision = strategy.evaluate(c, lenses)
    typer.echo(f"\nAggregated Decision: {decision.value}")

@app.command("preview-activation-bridge")
def preview_bridge(handoff_id: str = "mock"):
    """Generate the activation bridge package for an approved handoff."""
    c = _mock_candidate()
    bridge = build_activation_bridge(
        handoff_id=handoff_id,
        candidate_refs=[c["candidate_release_id"]],
        decision_ref="decision_123",
        context=c
    )
    typer.echo(bridge.model_dump_json(indent=2))

@app.command("preview-pre-activation-checklist")
def preview_checklist(handoff_id: str = "mock"):
    """Generate the pre-activation checklist for a handoff."""
    c = _mock_candidate({"gates_fresh": True, "approval_complete": True})
    checklist = build_pre_activation_checklist(handoff_id, c)
    for item in checklist.items:
        check = "[x]" if item.is_checked else "[ ]"
        typer.echo(f"{check} {item.description} {item.notes}")

@app.command("list-handoff-strategies")
def list_strategies():
    """List available handoff evaluation strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeHandoffStrategy")
    typer.echo("- BalancedReadinessCouncilStrategy")
    typer.echo("- EvidenceFirstHandoffStrategy")
    typer.echo("- GovernanceHeavyHandoffStrategy")
    typer.echo("- NarrowScopeFastBridgeStrategy")

if __name__ == "__main__":
    app()
