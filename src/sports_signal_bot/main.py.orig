import typer
from rich.console import Console

# Import the new assurance_exchange CLI app
from sports_signal_bot.assurance_exchange.cli import app as assurance_exchange_app

app = typer.Typer(help="Sports Signal Bot CLI")
console = Console()

app.add_typer(assurance_exchange_app, name="assurance-exchange", help="Assurance Exchange operations")

@app.command("smoke-run")
def smoke_run():
    console.print("Smoke run ok.")

if __name__ == "__main__":
    app()
