import typer
from rich.console import Console

# Import the new assurance_exchange CLI app
from sports_signal_bot.assurance_exchange.cli import app as assurance_exchange_app
from sports_signal_bot.cli_evidence_atlas import app as evidence_atlas_app

app = typer.Typer(help="Sports Signal Bot CLI")
console = Console()

app.add_typer(assurance_exchange_app, name="assurance-exchange", help="Assurance Exchange operations")
app.add_typer(evidence_atlas_app, name="evidence-atlas", help="Evidence Atlas operations")

@app.command("smoke-run")
def smoke_run():
    console.print("Smoke run ok.")

from sports_signal_bot.cli_proof_catalogs import app as proof_catalogs_app
app.add_typer(proof_catalogs_app, name="proof-catalogs", help="Phase 93: Proof Catalogs")

if __name__ == "__main__":
    app()
