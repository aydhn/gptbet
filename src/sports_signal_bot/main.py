from sports_signal_bot.cli.execution_coordination import app as execution_coordination_app
from sports_signal_bot.cli.live_execution_cli import app as live_execution_app
from sports_signal_bot.remediation_lanes.cli import remediation_lanes_app
import typer
from sports_signal_bot.cli.resilience_advisor import app as resilience_advisor_app
from sports_signal_bot.cli.remediation_copilot import app as copilot_app

app = typer.Typer()
app.add_typer(resilience_advisor_app, name="resilience-advisor")
app.add_typer(copilot_app, name="remediation-copilot")

app.add_typer(remediation_lanes_app, name="remediation-lanes", help="Phase 71: Remediation Lane Architecture")
app.add_typer(live_execution_app, name="live-execution", help="Live execution operations")
app.add_typer(execution_coordination_app, name="execution-coordination")

if __name__ == "__main__":
    app()
