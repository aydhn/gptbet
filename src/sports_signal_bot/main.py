import typer
from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app
from sports_signal_bot.cli.remediation_copilot import app as copilot_app
from sports_signal_bot.remediation_lanes.cli import app as lanes_app

app = typer.Typer()
app.add_typer(resilience_advisor_app, name="resilience-advisor")
app.add_typer(copilot_app, name="remediation-copilot")
app.add_typer(lanes_app, name="remediation-lanes")

if __name__ == "__main__":
    app()
