import typer
from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app

app = typer.Typer()
app.add_typer(resilience_advisor_app, name="resilience-advisor")

if __name__ == "__main__":
    app()
