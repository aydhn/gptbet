import sys

content = """from sports_signal_bot.remediation_lanes.cli import remediation_lanes_app
import typer
from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app
from sports_signal_bot.cli.remediation_copilot import app as copilot_app

app = typer.Typer()
app.add_typer(resilience_advisor_app, name="resilience-advisor")
app.add_typer(copilot_app, name="remediation-copilot")

app.add_typer(remediation_lanes_app, name="remediation-lanes", help="Phase 71: Remediation Lane Architecture")

if __name__ == "__main__":
    app()
"""

with open("src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
