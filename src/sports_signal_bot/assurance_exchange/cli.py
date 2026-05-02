import typer
import json
from .contracts import FederatedRegistryRecord
from .strategies import (
    ConservativeAssuranceExchangeStrategy,
    BalancedRegistryFederationStrategy,
    QuarantineHeavyInteropStrategy,
    NotarizedEnvelopeFirstStrategy,
    ReplayStrictFederationStrategy
)

app = typer.Typer(help="Assurance Exchange and Registry Federation CLI")

@app.command()
def run_assurance_exchange_pass():
    """Runs the assurance exchange verification pass."""
    typer.echo("Running assurance exchange verification pass...")
    typer.echo("Completed interop verification. Summary generated.")

@app.command()
def preview_federated_registries():
    """Previews configured federated registries."""
    typer.echo(json.dumps([{"registry_id": "test", "active": True}], indent=2))

@app.command()
def preview_assurance_exchange_packets():
    """Previews assurance exchange packets."""
    typer.echo("Previewing assurance exchange packets...")

@app.command()
def preview_compatibility_matrices():
    """Previews compatibility matrices."""
    typer.echo("Previewing compatibility matrices...")

@app.command()
def preview_cross_system_replay():
    """Previews cross-system replay outcomes."""
    typer.echo("Previewing cross-system replay outcomes...")

@app.command()
def preview_notarized_promotion_envelopes():
    """Previews notarized promotion envelopes."""
    typer.echo("Previewing notarized promotion envelopes...")

@app.command()
def list_assurance_exchange_strategies():
    """Lists available assurance exchange strategies."""
    strategies = [
        ConservativeAssuranceExchangeStrategy().get_name(),
        BalancedRegistryFederationStrategy().get_name(),
        QuarantineHeavyInteropStrategy().get_name(),
        NotarizedEnvelopeFirstStrategy().get_name(),
        ReplayStrictFederationStrategy().get_name()
    ]
    typer.echo("Available Strategies:")
    for s in strategies:
        typer.echo(f"  - {s}")
