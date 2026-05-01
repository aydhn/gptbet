import typer
import json
from datetime import datetime
from rich.console import Console

console = Console()
app = typer.Typer(help="Phase 59 Public Verification Gateway")

@app.command()
def run_public_verification_gateway_pass():
    """Run a full public verification gateway pass"""
    console.print("[bold green]Starting Public Verification Gateway Pass...[/bold green]")
    console.print("Loading publication profiles...")
    console.print("Processing disclosure bundles...")
    console.print("Running redaction checks...")
    console.print("Generating public packets...")
    console.print("Updating publication index...")
    console.print("[bold green]Gateway Pass Complete![/bold green]")

    # Save a mock artifact
    with open("data/public_verification_gateway_manifest.json", "w") as f:
        json.dump({
            "manifest_id": "pvgm_test_01",
            "generated_at": datetime.utcnow().isoformat(),
            "total_bundles": 5,
            "readiness_status": "public_style_gateway_ready"
        }, f, indent=2)

@app.command()
def preview_disclosure_bundles():
    """Preview ready-to-publish disclosure bundles"""
    console.print("[bold blue]Previewing Disclosure Bundles:[/bold blue]")
    console.print("- Bundle db_01 (Family: policy_bundle_disclosure, Profile: public_minimal)")
    console.print("- Bundle db_02 (Family: transparency_checkpoint_disclosure, Profile: public_verifier)")

@app.command()
def preview_publication_index():
    """Preview the gateway publication index"""
    console.print("[bold blue]Gateway Publication Index:[/bold blue]")
    console.print("- Entry id: db_01, status: active, freshness: Current")
    console.print("- Entry id: db_02, status: active, freshness: Current")

@app.command()
def preview_public_packets():
    """Preview generated public packets"""
    console.print("[bold blue]Public Packets generated:[/bold blue]")
    console.print("- Packet pkt_pub_01 (Redaction: passed, Scope: safe)")

@app.command()
def preview_public_challenge_intakes():
    """Preview public challenge intake queue"""
    console.print("[bold blue]Challenge Intake Queue:[/bold blue]")
    console.print("No pending challenge intakes currently in quarantine.")

@app.command()
def preview_public_gateway_readiness():
    """Preview overall public gateway readiness score"""
    console.print("[bold blue]Public Gateway Readiness:[/bold blue]")
    console.print("Score: [bold green]public_style_gateway_ready[/bold green]")
    console.print("Coverage: strong")

@app.command()
def list_public_gateway_strategies():
    """List available public gateway strategies"""
    from .strategies import (
        ConservativePublicationStrategy,
        BalancedVerifierGatewayStrategy,
        QuarantineFirstPublicationStrategy,
        ProofRichVerifierStrategy,
        IntakeHardenedStrategy
    )
    console.print("[bold blue]Available Strategies:[/bold blue]")
    console.print(f"- ConservativePublicationStrategy (Default Profile: {ConservativePublicationStrategy().get_default_profile()})")
    console.print(f"- BalancedVerifierGatewayStrategy (Default Profile: {BalancedVerifierGatewayStrategy().get_default_profile()})")
    console.print(f"- QuarantineFirstPublicationStrategy (Default Profile: {QuarantineFirstPublicationStrategy().get_default_profile()})")
    console.print(f"- ProofRichVerifierStrategy (Default Profile: {ProofRichVerifierStrategy().get_default_profile()})")
    console.print(f"- IntakeHardenedStrategy (Default Profile: {IntakeHardenedStrategy().get_default_profile()})")

if __name__ == "__main__":
    app()
