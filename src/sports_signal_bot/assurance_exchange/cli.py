import typer
from rich.console import Console
from .dashboard_exchanges import build_assurance_dashboard_exchange, summarize_dashboard_exchange
from .federation_boards import build_council_federation_board, summarize_federation_board
from .replay_clearing import build_replay_market_clearing_layer, summarize_replay_clearing
from .planners import build_debt_settlement_planner_v2, summarize_settlement_planner_v2
from .dashboards import build_governance_assurance_dashboard_v2, summarize_dashboard_health_v2
from .narratives import build_governance_narrative_compiler, compile_governance_narrative, summarize_narrative_output

app = typer.Typer(help="Assurance Exchange operations")
console = Console()

@app.command("run-assurance-exchange-pass")
def run_assurance_exchange_pass():
    """Run a full assurance exchange pass."""
    console.print("[green]Running Assurance Exchange pass...[/green]")

    # Simulate the pass
    dashboard = build_assurance_dashboard_exchange(
        source_dashboard_refs=["sd_1"],
        source_snapshot_refs=["ss_1"],
        exchange_scope="full",
        audience_profile_refs=["ap_1"]
    )
    console.print(f"Built Dashboard Exchange: {summarize_dashboard_exchange(dashboard)}")

    board = build_council_federation_board("synthesis_federation_board", ["mc_1"], "q_pol_1")
    console.print(f"Built Federation Board: {summarize_federation_board(board)}")

    layer = build_replay_market_clearing_layer("bounded_replay_clearing_layer")
    console.print(f"Built Replay Market Clearing Layer: {summarize_replay_clearing(layer)}")

    planner = build_debt_settlement_planner_v2("replay_first_settlement_planner")
    console.print(f"Built Debt Settlement Planner: {summarize_settlement_planner_v2(planner)}")

    assurance_dashboard = build_governance_assurance_dashboard_v2("operator_assurance_dashboard")
    console.print(f"Built Assurance Dashboard: {summarize_dashboard_health_v2(assurance_dashboard)}")

    compiler = build_governance_narrative_compiler("operator_narrative_compiler")
    output = compile_governance_narrative(compiler)
    console.print(f"Compiled Governance Narrative: {summarize_narrative_output(output)}")

    console.print("[green]Assurance Exchange pass completed successfully.[/green]")

@app.command("preview-dashboard-exchanges")
def preview_dashboard_exchanges():
    """Preview current dashboard exchanges."""
    console.print("[blue]Previewing Dashboard Exchanges...[/blue]")
    dashboard = build_assurance_dashboard_exchange(
        source_dashboard_refs=["sd_1"],
        source_snapshot_refs=["ss_1"],
        exchange_scope="full",
        audience_profile_refs=["ap_1"]
    )
    console.print(summarize_dashboard_exchange(dashboard))

@app.command("preview-federation-boards")
def preview_federation_boards():
    """Preview current federation boards."""
    console.print("[blue]Previewing Federation Boards...[/blue]")
    board = build_council_federation_board("synthesis_federation_board", ["mc_1"], "q_pol_1")
    console.print(summarize_federation_board(board))

@app.command("preview-replay-clearing")
def preview_replay_clearing():
    """Preview current replay market clearing state."""
    console.print("[blue]Previewing Replay Market Clearing...[/blue]")
    layer = build_replay_market_clearing_layer("bounded_replay_clearing_layer")
    console.print(summarize_replay_clearing(layer))

@app.command("preview-assurance-narratives")
def preview_assurance_narratives():
    """Preview current governance narratives."""
    console.print("[blue]Previewing Governance Narratives...[/blue]")
    compiler = build_governance_narrative_compiler("operator_narrative_compiler")
    output = compile_governance_narrative(compiler)
    console.print(summarize_narrative_output(output))

@app.command("list-assurance-exchange-strategies")
def list_assurance_exchange_strategies():
    """List available assurance exchange strategies."""
    from .strategies.conservative import ConservativeNarrativeAssuranceStrategy
    from .strategies.balanced_board_clearing import BalancedBoardClearingStrategy
    from .strategies.debt_settlement_narrative_first import DebtSettlementNarrativeFirstStrategy

    strategies = [
        ConservativeNarrativeAssuranceStrategy().name,
        BalancedBoardClearingStrategy().name,
        DebtSettlementNarrativeFirstStrategy().name
    ]
    console.print("[yellow]Available Strategies:[/yellow]")
    for s in strategies:
        console.print(f"- {s}")
