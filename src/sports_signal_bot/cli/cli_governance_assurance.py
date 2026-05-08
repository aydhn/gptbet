import typer
import json
import os
from sports_signal_bot.governance_assurance.contracts import (
    CouncilFamily,
    ReplayMarketplaceFamily,
    PlannerFamily,
    DashboardFamily
)
from sports_signal_bot.governance_assurance.synthesis_councils import build_resilience_synthesis_council, summarize_synthesis_council
from sports_signal_bot.governance_assurance.replay_marketplaces import build_replay_exchange_marketplace, summarize_replay_marketplace
from sports_signal_bot.governance_assurance.settlement_planners import build_debt_settlement_planner, summarize_settlement_planner
from sports_signal_bot.governance_assurance.dashboards import build_governance_assurance_dashboard, summarize_dashboard_health

app = typer.Typer()

@app.command("run-governance-assurance-pass")
def run_governance_assurance_pass():
    typer.echo("Running governance assurance pass...")

    council = build_resilience_synthesis_council("c1", CouncilFamily.SYNTHESIS_BAND_REVIEW, ["s1"])
    marketplace = build_replay_exchange_marketplace("m1", ReplayMarketplaceFamily.BOUNDED_REPLAY)
    planner = build_debt_settlement_planner("p1", PlannerFamily.MIXED_DEBT_REDUCTION, ["d1"])
    dashboard = build_governance_assurance_dashboard("d1", DashboardFamily.EXECUTIVE_SUMMARY)

    os.makedirs("results", exist_ok=True)
    with open("results/governance_assurance_summary.json", "w") as f:
        json.dump({
            "council": summarize_synthesis_council(council),
            "marketplace": summarize_replay_marketplace(marketplace),
            "planner": summarize_settlement_planner(planner),
            "dashboard": summarize_dashboard_health(dashboard)
        }, f, indent=2, default=str)

    typer.echo("Pass complete. Summary written to results/governance_assurance_summary.json")

@app.command("preview-synthesis-councils")
def preview_synthesis_councils():
    typer.echo("Previewing synthesis councils...")

@app.command("preview-replay-marketplaces")
def preview_replay_marketplaces():
    typer.echo("Previewing replay marketplaces...")

@app.command("preview-settlement-plans")
def preview_settlement_plans():
    typer.echo("Previewing settlement plans...")

@app.command("preview-assurance-dashboards")
def preview_assurance_dashboards():
    typer.echo("Previewing assurance dashboards...")

@app.command("preview-governance-assurance-health")
def preview_governance_assurance_health():
    typer.echo("Previewing governance assurance health...")

@app.command("list-governance-assurance-strategies")
def list_governance_assurance_strategies():
    typer.echo("Available strategies:")
    typer.echo(" - ConservativeAssuranceDashboardStrategy")
    typer.echo(" - BalancedCouncilMarketplaceStrategy")
    typer.echo(" - DebtPlannerFirstStrategy")
    typer.echo(" - ReplayMarketplaceStrictStrategy")
    typer.echo(" - SovereigntyDominantAssuranceStrategy")

if __name__ == "__main__":
    app()
