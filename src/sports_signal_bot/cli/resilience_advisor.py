import typer
from rich.console import Console
from rich.table import Table
import json

app = typer.Typer(help="Resilience Advisor and Recovery Orchestration operations.")
console = Console()

@app.command("run-resilience-advisor-pass")
def run_resilience_advisor_pass():
    """Run a complete resilience advisor and playbook synthesis pass."""
    console.print("[bold green]Running resilience advisor pass...[/bold green]")
    from sports_signal_bot.resilience_advisor.memory import FailurePatternMemory
    from sports_signal_bot.resilience_advisor.strategies.balanced_playbook_synthesis import BalancedPlaybookSynthesisStrategy

    memory = FailurePatternMemory()
    # Dummy mock data
    incident_signals = {
        "incident_ref": "inc_123",
        "source_family": "odds_api",
        "event_families": ["football"],
        "swarm_agreement_status": "split_brain"
    }

    strategy = BalancedPlaybookSynthesisStrategy(memory)
    advice = strategy.synthesize_advice(incident_signals)

    console.print(f"Generated Advisory Recommendation: [cyan]{advice.recommendation_id}[/cyan]")
    console.print(f"Decision Type: [yellow]{advice.decision_type}[/yellow]")
    console.print(f"Confidence Band: [magenta]{advice.confidence.confidence_band}[/magenta]")
    console.print(f"Plan Ref: [blue]{advice.plan_ref}[/blue]")
    console.print("[bold green]Pass complete.[/bold green]")

@app.command("preview-failure-pattern-memory")
def preview_failure_pattern_memory():
    """Preview the failure pattern memory."""
    console.print("[bold blue]Previewing Failure Pattern Memory...[/bold blue]")
    table = Table("Pattern ID", "Family", "Root Cause", "Outcome")
    # Dummy row
    table.add_row("pat_456", "sync_recovery", "stale_source", "recovered_in_5m")
    console.print(table)

@app.command("preview-pattern-matches")
def preview_pattern_matches():
    """Preview recent pattern matches for active incidents."""
    console.print("[bold blue]Previewing Pattern Matches...[/bold blue]")
    table = Table("Incident Ref", "Top Match Pattern", "Similarity Score", "Band")
    # Dummy row
    table.add_row("inc_123", "pat_456", "0.85", "strong_match")
    console.print(table)

@app.command("preview-remediation-playbooks")
def preview_remediation_playbooks():
    """Preview synthesized remediation playbooks."""
    console.print("[bold blue]Previewing Remediation Playbooks...[/bold blue]")
    table = Table("Playbook ID", "Target Family", "Steps", "Risks")
    # Dummy row
    table.add_row("pb_789", "quarantine_recovery", "2", "medium")
    console.print(table)

@app.command("preview-recovery-orchestration-plans")
def preview_recovery_orchestration_plans():
    """Preview recovery orchestration plans."""
    console.print("[bold blue]Previewing Recovery Orchestration Plans...[/bold blue]")
    table = Table("Plan ID", "Incident Ref", "Playbook Ref", "Bounded")
    # Dummy row
    table.add_row("plan_101", "inc_123", "pb_789", "True")
    console.print(table)

@app.command("preview-advisory-confidence")
def preview_advisory_confidence():
    """Preview confidence distributions for recent advice."""
    console.print("[bold blue]Previewing Advisory Confidence...[/bold blue]")
    table = Table("Recommendation ID", "Decision", "Confidence Band", "Score")
    # Dummy row
    table.add_row("rec_202", "recommend_playbook", "moderate", "0.65")
    console.print(table)

@app.command("list-resilience-advisor-strategies")
def list_resilience_advisor_strategies():
    """List available resilience advisor strategies."""
    console.print("[bold blue]Available Resilience Advisor Strategies:[/bold blue]")
    strategies = [
        "ConservativeRecoveryAdvisorStrategy (quarantine-first, review-heavy)",
        "BalancedPlaybookSynthesisStrategy (default, balanced pattern reuse)",
        "PatternMemoryFirstStrategy (relies heavily on historical memory)"
    ]
    for s in strategies:
        console.print(f"- [green]{s}[/green]")

if __name__ == "__main__":
    app()
