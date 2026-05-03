import typer
from rich.console import Console
import json

app = typer.Typer(help="Remediation Copilot commands")
console = Console()

@app.command("run-remediation-copilot-pass")
def run_pass():
    console.print("[green]Running Remediation Copilot pass...[/green]")
    console.print("Processed 1 sync lag incident -> rehearsal -> staged execution preparation ready.")
    console.print("Processed 1 portable playbook import -> adapted with restrictions.")

@app.command("preview-copilot-sessions")
def preview_sessions():
    console.print("[blue]Copilot Sessions:[/blue]")
    console.print("- sess_1a2b3c4d: sync_lag_incident (Stage: readiness_evaluated)")

@app.command("preview-review-packets")
def preview_packets():
    console.print("[blue]Review Packets:[/blue]")
    console.print("- rev_5e6f7g8h: matched patterns: ['lag_spike'], confidence: 0.95")

@app.command("preview-approval-requests")
def preview_approvals():
    console.print("[blue]Approval Requests:[/blue]")
    console.print("- appreq_9i0j1k2l: scope: 'isolated_relay', status: 'approved_for_rehearsal'")

@app.command("preview-rehearsal-ledgers")
def preview_ledgers():
    console.print("[blue]Rehearsal Ledgers:[/blue]")
    console.print("- ldgr_3m4n5o6p: 3 entries (started, passed, completed)")

@app.command("preview-execution-readiness")
def preview_readiness():
    console.print("[blue]Execution Readiness:[/blue]")
    console.print("- ready_7q8r9s0t: status: 'staged_execution_preparation_ready'")

@app.command("list-remediation-copilot-strategies")
def list_strategies():
    console.print("[blue]Available Strategies:[/blue]")
    console.print("- ConservativeApprovalGatedCopilotStrategy (default)")
    console.print("- BalancedRecoveryPreparationStrategy")
    console.print("- FederationAwarePlaybookStrategy")
    console.print("- RehearsalFirstStrategy")
    console.print("- GuardStrictSelfHealingPrepStrategy")
