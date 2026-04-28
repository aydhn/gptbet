import uuid
import typer
from typing import Optional
from sports_signal_bot.release_management.contracts import PromotionRequestRecord, RequestType
from sports_signal_bot.release_management.runner import ReleaseRunner
from sports_signal_bot.release_management.registry import StrategyRegistry
from sports_signal_bot.release_management.state import ChannelStateManager
from sports_signal_bot.release_management.rollback import RollbackPlanner

app = typer.Typer(help="Release Management Commands")


@app.command(name="run-release", help="Execute a promotion or rollback request")
def run_release(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    strategy: str = typer.Option("conservative_promotion", help="Release strategy to use"),
    mode: str = typer.Option("ops", help="dry_run or ops mode"),
):
    typer.echo(f"Running release for {sport} {market} using {strategy} strategy (Mode: {mode})")

    # Normally this would determine request type based on current state (e.g., candidate -> canary, canary -> stable)
    # Mocking a candidate -> canary request
    runner = ReleaseRunner()

    request = PromotionRequestRecord(
        request_id=str(uuid.uuid4()),
        request_type=RequestType.promote_candidate_to_canary,
        sport=sport,
        market_type=market,
        target_chain_group_id=f"chain_{sport}_{market}_candidate_1",
        requested_by="cli_user",
        rationale="Running CLI promotion command.",
    )

    if mode == "dry_run":
        typer.echo("[Dry Run] Promotion decision engine check...")
        decision = runner.decision_engine.evaluate_request(request)
        typer.echo(f"Decision: {decision.decision}")
        typer.echo(f"Rationale: {decision.rationale}")
        for g in decision.guards_evaluated:
            typer.echo(f"  Guard {g.guard_name}: {'Passed' if g.passed else 'Failed'} - {g.reason}")
    else:
        result = runner.process_request(request, strategy)
        typer.echo(f"Executed Request. Result status or decision output: {result}")


@app.command(name="preview-release-channels", help="Preview the current active channels for a market")
def preview_release_channels(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing release channels for {sport} {market}")
    state_manager = ChannelStateManager()
    state = state_manager.get_active_channel_state(sport, market)

    typer.echo(f"  Active Stable: {state.active_stable_chain_id or 'None'}")
    typer.echo(f"  Active Canary: {state.active_canary_chain_id or 'None'}")
    typer.echo(f"  Previous Stable: {state.previous_stable_chain_id or 'None'}")
    typer.echo(f"  Quarantined: {len(state.quarantined_artifacts)}")
    typer.echo(f"  Frozen: {state.frozen_channel_flags.get('system', False)}")


@app.command(name="preview-canary-status", help="Preview current canary validation status")
def preview_canary_status(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing canary status for {sport} {market}")
    state_manager = ChannelStateManager()
    state = state_manager.get_active_channel_state(sport, market)

    if not state.active_canary_chain_id:
        typer.echo("No active canary.")
        return

    typer.echo(f"Canary {state.active_canary_chain_id} is running.")
    typer.echo("Status: evaluating metrics... (Mock: Pass with warnings)")


@app.command(name="preview-rollback-plan", help="Preview rollback plan for a market")
def preview_rollback_plan(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing rollback plan for {sport} {market}")
    state_manager = ChannelStateManager()
    planner = RollbackPlanner(state_manager)
    plan = planner.create_rollback_plan(sport, market, "preview")

    if plan:
        typer.echo(f"Rollback Target: {plan.target.chain_group_id}")
        typer.echo(f"Known Safe: {plan.target.known_safe}")
        typer.echo(f"Validation Passed: {plan.validation.target_valid}")
    else:
        typer.echo("No rollback plan could be generated (missing previous stable?).")


@app.command(name="list-release-strategies", help="List all release strategies")
def list_release_strategies():
    typer.echo("Available Release Strategies:")
    for s in StrategyRegistry.list_strategies():
        typer.echo(f"  - {s}")
