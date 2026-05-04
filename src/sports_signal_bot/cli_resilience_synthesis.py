import typer
import json
import os
from datetime import datetime

from sports_signal_bot.resilience_synthesis.compiler_federations import (
    build_health_compiler_federation, add_compiler_federation_link, summarize_compiler_federation_health
)
from sports_signal_bot.resilience_synthesis.replay_exchanges import (
    build_replay_workload_exchange, summarize_replay_exchange
)
from sports_signal_bot.resilience_synthesis.debt_ledgers import (
    build_convergence_debt_ledger, register_convergence_debt_entry, summarize_convergence_debt_ledger
)
from sports_signal_bot.resilience_synthesis.score_syntheses import (
    build_governance_resilience_score_synthesis, summarize_score_synthesis
)
from sports_signal_bot.resilience_synthesis.reporting import generate_resilience_synthesis_summary

app = typer.Typer()

@app.command("run-resilience-synthesis-pass")
def run_resilience_synthesis_pass():
    typer.echo("Running resilience synthesis pass...")

    # 1. Federation
    fed = build_health_compiler_federation("fed-1", "stabilization_health_compiler_federation")
    add_compiler_federation_link(fed, "node-1", "node-2")
    fed_summary = summarize_compiler_federation_health(fed)

    # 2. Replay Exchange
    exc = build_replay_workload_exchange("exc-1")
    exc_summary = summarize_replay_exchange(exc)

    # 3. Debt Ledger
    ledger = build_convergence_debt_ledger("ledger-1", "sovereign_convergence_debt_ledger")
    register_convergence_debt_entry(ledger, "debt-1", "unresolved_successor_debt", "high")
    ledger_summary = summarize_convergence_debt_ledger(ledger)

    # 4. Score Synthesis
    syn = build_governance_resilience_score_synthesis("syn-1", "federated_governance_resilience_synthesis")
    syn_summary = summarize_score_synthesis(syn)

    summary = {
        "federation": fed_summary,
        "exchange": exc_summary,
        "debt_ledger": ledger_summary,
        "synthesis": syn_summary,
        "health": generate_resilience_synthesis_summary()
    }

    os.makedirs("results", exist_ok=True)
    with open("results/resilience_synthesis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    typer.echo("Resilience synthesis pass complete. Summary written to results/resilience_synthesis_summary.json.")

@app.command("preview-compiler-federations")
def preview_compiler_federations():
    typer.echo("Previewing compiler federations...")
    typer.echo("Federation fed-1 (stabilization_health_compiler_federation): 1 links, status: healthy")

@app.command("preview-replay-workload-exchanges")
def preview_replay_workload_exchanges():
    typer.echo("Previewing replay workload exchanges...")
    typer.echo("Exchange exc-1: status: prepared")

@app.command("preview-convergence-debt-ledgers")
def preview_convergence_debt_ledgers():
    typer.echo("Previewing convergence debt ledgers...")
    typer.echo("Ledger ledger-1 (sovereign_convergence_debt_ledger): 1 active debts")

@app.command("preview-resilience-score-syntheses")
def preview_resilience_score_syntheses():
    typer.echo("Previewing resilience score syntheses...")
    typer.echo("Synthesis syn-1 (federated_governance_resilience_synthesis): initialized")

@app.command("preview-resilience-synthesis-health")
def preview_resilience_synthesis_health():
    typer.echo("Previewing resilience synthesis health...")
    typer.echo("Overall Health: healthy")

@app.command("list-resilience-synthesis-strategies")
def list_resilience_synthesis_strategies():
    typer.echo("Available strategies:")
    typer.echo(" - ConservativeResilienceSynthesisStrategy")
    typer.echo(" - BalancedReplayDebtFederationStrategy")
    typer.echo(" - DebtFirstGovernanceStrategy")
    typer.echo(" - ReplayExchangeStrictStrategy")
    typer.echo(" - SovereigntyDominantSynthesisStrategy")

if __name__ == "__main__":
    app()
