import typer
import json
from .bundles import build_signed_policy_bundle
from .ledger import get_ledger
from .verification import run_integrity_verification

app = typer.Typer(help="Phase 54 Governance Integrity")

@app.command()
def run_governance_integrity_check():
    """Runs a full integrity check on the governance ledger."""
    ledger = get_ledger()
    summary = ledger.summarize_ledger_integrity()
    typer.echo("--- Ledger Integrity Check ---")
    typer.echo(json.dumps(summary, indent=2))

@app.command()
def verify_policy_bundle(bundle_family: str, signer_id: str = "local_dev_signer"):
    """Creates and verifies a mock signed bundle."""
    payload = {"rules": ["rule1"]}
    bundle = build_signed_policy_bundle(payload, bundle_family, "1.0", signer_id)

    typer.echo("--- Bundle Created ---")
    typer.echo(f"ID: {bundle.signed_bundle_id}")

    res = run_integrity_verification(bundle, payload)
    typer.echo("\n--- Verification Result ---")
    typer.echo(json.dumps(res, indent=2))

@app.command()
def list_governance_integrity_strategies():
    """Lists available integrity strategies."""
    typer.echo("Available Integrity Strategies:")
    typer.echo("- ConservativeSignedGovernanceStrategy")
    typer.echo("- BalancedIntegrityStrategy")
    typer.echo("- ReviewFriendlyQuarantineStrategy")
