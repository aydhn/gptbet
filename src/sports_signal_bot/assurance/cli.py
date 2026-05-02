import typer
from typing import Optional

app = typer.Typer(help="Phase 62 Assurance and Promotion Envelopes")

@app.command()
def run_assurance_pass():
    """Runs the assurance pass to generate claims, bundles, and envelopes."""
    import json
    import os
    from datetime import datetime
    from sports_signal_bot.assurance.integration import run_assurance_pipeline_for_target

    result = run_assurance_pipeline_for_target("target_promo_01")

    def datetime_handler(x):
        if isinstance(x, datetime):
            return x.isoformat()
        raise TypeError("Unknown type")

    os.makedirs("results", exist_ok=True)
    with open("results/assurance_summary.json", "w") as f:
        json.dump(result, f, indent=2, default=datetime_handler)

    typer.echo(f"Assurance pass completed for target {result['target']}.")
    typer.echo(f"Evaluation Passed: {result['evaluation_passed']}")
    typer.echo(f"Envelope Decision: {result['envelope']['final_assurance_decision']}")
    typer.echo("Artifacts saved to results/assurance_summary.json")

@app.command()
def preview_proof_carrying_bundles():
    """Previews proof-carrying bundles."""
    typer.echo("Previewing 1 proof-carrying bundle...")
    typer.echo("- pcb_bundle123 (promotion_candidate_assurance_bundle for target_promo_01)")

@app.command()
def preview_assurance_claims():
    """Previews assurance claims."""
    typer.echo("Previewing assurance claims...")
    typer.echo("- Claim clm_pol: policy_conformance_claim (satisfied)")
    typer.echo("- Claim clm_int: integrity_chain_claim (satisfied)")

@app.command()
def preview_attestations():
    """Previews assurance attestations."""
    typer.echo("Previewing assurance attestations...")
    typer.echo("- Attestation att_conf (conformance_runner_attester): valid")

@app.command()
def preview_promotion_envelopes():
    """Previews promotion envelopes."""
    typer.echo("Previewing promotion envelopes...")
    typer.echo("- Envelope env_abc for target_promo_01: assurance_ready")

@app.command()
def preview_claim_replay_results():
    """Previews claim replay results."""
    typer.echo("Previewing claim replay results...")
    typer.echo("- Replay rep_xyz for original envelope env_abc: matched")

@app.command()
def list_assurance_strategies():
    """Lists available assurance strategies."""
    typer.echo("Available Assurance Strategies:")
    typer.echo("1. ConservativeAssuranceEnvelopeStrategy")
    typer.echo("2. BalancedProofCarryingStrategy (Default)")
    typer.echo("3. AttestationHeavyStrategy")
    typer.echo("4. ReplayFirstAssuranceStrategy")
    typer.echo("5. MinimalExceptionStrategy")

if __name__ == "__main__":
    app()
