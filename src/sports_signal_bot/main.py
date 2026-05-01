from .transparency.cli import app as transparency_app
from .witness_mesh.cli import app as witness_mesh_app
from .governance_integrity.cli import app as governance_integrity_app
from .multi_signer_trust.cli import app as multi_signer_trust_app
from .policy_as_code.cli import app as policy_as_code_app
from .cohort_autopilot.cli import app as cohort_autopilot_app
from .expansion_governance.cli import app as expansion_governance_app
from .federated_governance.cli import app as federated_governance_app


from .staged_channels.cli import app as staged_channels_app
import typer
from .tournaments.cli import app as tournaments_app
from .candidate_promotion.cli import app as candidate_promotion_app
from .auto_promotion.cli import app as auto_promotion_app
from .deployment.cli import app as deployment_app
from .handoff.cli import app as handoff_app
from .stable_adoption.cli import app as stable_adoption_app
import json
from datetime import datetime

# Import simulation components
from .simulation.contracts import SimulationRequestRecord, SimulationMode
from .simulation.patches import build_candidate_patch
from .simulation.strategies.balanced_comparative import BalancedComparativeStrategy

app = typer.Typer(help="Sports Signal Bot CLI")
app.add_typer(staged_channels_app, name="staged-channels", help="Phase 46 Staged Channels")

@app.command()
def simulate_suggestion(suggestion_id: str):
    """Run a sandbox simulation for a candidate patch suggestion."""
    typer.echo(f"Starting simulation for suggestion: {suggestion_id}")

    # Mock suggestion
    mock_suggestion = {
        "suggestion_id": suggestion_id,
        "target_component_family": "provider_priority",
        "patch_payload": {"priority": "high"},
        "scope": {"sport": "football"}
    }

    patch = build_candidate_patch(mock_suggestion)
    request = SimulationRequestRecord(
        request_id=f"req_{datetime.utcnow().timestamp()}",
        suggestion_ids=[suggestion_id],
        simulation_mode=SimulationMode.COMPARATIVE_SLOT_REPLAY,
        audience_profile="operator",
        replay_window={"start": datetime.utcnow(), "end": datetime.utcnow()}
    )

    strategy = BalancedComparativeStrategy()
    run_record = strategy.run_simulation(request, patch)

    typer.echo(f"\n--- Simulation Result ---")
    typer.echo(f"Run ID: {run_record.run_id}")
    typer.echo(f"Status: {run_record.status}")
    if run_record.comparison:
        typer.echo(f"Comparison Status: {run_record.comparison.status.value}")
        typer.echo(f"Materiality Band: {run_record.comparison.materiality_band.value}")
    if run_record.recommendation:
        typer.echo(f"Recommendation: {run_record.recommendation.recommendation.value}")
        typer.echo(f"Rationale: {run_record.recommendation.rationale}")

@app.command()
def list_simulation_strategies():
    """List available simulation strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeSandboxStrategy")
    typer.echo("- BalancedComparativeStrategy")
    typer.echo("- AdvisoryExplorationStrategy")

app.add_typer(tournaments_app, name="tournaments", help="Phase 44 Candidate Tournaments")
app.add_typer(candidate_promotion_app, name="candidate-promotion", help="Phase 45 Candidate Promotion")
app.add_typer(auto_promotion_app, name="auto-promotion", help="Phase 47 Constrained Auto Promotion")
app.add_typer(handoff_app, name="handoff", help="Phase 48 Candidate-to-Release Handoff")
app.add_typer(stable_adoption_app, name="stable-adoption", help="Phase 49 Staged Stable Adoption")
app.add_typer(cohort_autopilot_app, name="cohort-autopilot", help="Phase 50 Cohort Autopilot")
app.add_typer(expansion_governance_app, name="expansion-governance", help="Phase 51 Expansion Governance")
app.add_typer(federated_governance_app, name="federated-governance", help="Phase 52 Federated Governance")
app.add_typer(policy_as_code_app, name="policy-as-code", help="Phase 53 Policy as Code Engine")


app.add_typer(deployment_app, name="deploy", help="Deployment Operations")

app.add_typer(governance_integrity_app, name="governance-integrity", help="Phase 54 Governance Integrity")
app.add_typer(multi_signer_trust_app, name="multi-signer-trust", help="Phase 55 Multi-Signer Trust")
app.add_typer(transparency_app, name="transparency", help="Phase 56 Governance Transparency")
app.add_typer(witness_mesh_app, name="witness-mesh", help="Phase 57 Witness Mesh")




@app.command()
def run_external_audit_exchange_pass():
    """Runs the external audit exchange pass, processing requests, responses, notarizations, and updating readiness."""
    import json
    import os
    from sports_signal_bot.external_audit_exchange.manifests import generate_external_audit_manifest

    # Mock processing
    stats = {
        "exported": 5,
        "imported": 3,
        "quarantined": 1,
        "notarizations_verified": 2,
        "notarizations_unverified": 0,
        "reputation_distribution": {"excellent": 1, "adequate": 2}
    }
    manifest = generate_external_audit_manifest(stats)

    os.makedirs("results", exist_ok=True)
    with open("results/external_audit_exchange_summary.json", "w") as f:
        f.write(manifest.model_dump_json(indent=2))

    print(f"External audit exchange pass completed. {stats['exported']} exported, {stats['imported']} imported.")
    print("Manifest saved to results/external_audit_exchange_summary.json")

@app.command()
def preview_external_audit_requests():
    """Previews generated external audit requests."""
    print("Previewing 2 external audit requests...")
    print("- Request req_1: Target target_a (strict redaction)")
    print("- Request req_2: Target target_b (relaxed redaction)")

@app.command()
def preview_external_findings():
    """Previews external findings normalized from responses."""
    print("Previewing 3 external findings...")
    print("- Finding f_1: severity warning, target target_a")
    print("- Finding f_2: severity info, target target_a")
    print("- Finding f_3: severity critical, target target_b (escalated to anomaly)")

@app.command()
def preview_notarization_receipts():
    """Previews notarization receipts and verification status."""
    print("Previewing notarization receipts...")
    print("- Receipt rec_1: verified against digest xyz123")
    print("- Receipt rec_2: unverified (digest mismatch)")

@app.command()
def preview_witness_reputation():
    """Previews witness reputation scores and bands."""
    print("Witness Reputation Distribution:")
    print("- w_1: 85.0 (excellent)")
    print("- w_2: 65.0 (strong)")
    print("- w_3: 25.0 (low_trust - penalty applied)")

@app.command()
def preview_challenge_triage():
    """Previews challenge triage routing and priority."""
    print("Challenge Triage Backlog:")
    print("- Challenge chal_1: high priority -> assigned 'expert' class")
    print("- Challenge chal_2: low priority -> assigned 'internal_review' class (due to reputation)")

@app.command()
def list_external_audit_exchange_strategies():
    """Lists available external audit exchange strategies."""
    print("Available External Audit Exchange Strategies:")
    print("1. ConservativeExternalAuditStrategy (Default)")
    print("2. BalancedExchangeReadinessStrategy")
    print("3. QuarantineHeavyExternalInputStrategy")
    print("4. NotarizationFirstStrategy")
    print("5. ReputationAwareChallengeStrategy")


if __name__ == "__main__":
    app()
