from typing import Optional

import typer
from sports_signal_bot.inference.runner import InferenceRunner

app = typer.Typer(help="Live-like inference execution and orchestration")


@app.command(name="run-inference", help="Execute an end-to-end inference snapshot")
def run_inference(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    slot: Optional[str] = typer.Option(
        None, help="Slot identifier (morning/midday/evening)"
    ),
    mode: str = typer.Option(
        "research_live_like_mode", help="Inference execution mode"
    ),
):
    typer.echo(
        f"Initializing Inference Runner for {sport} - {market} (Slot: {slot}, Mode: {mode})"
    )
    runner = InferenceRunner()

    result = runner.run(sport, market, slot_name=slot, mode=mode)

    if not result:
        typer.echo("Inference run aborted or returned no results.")
        return

    manifest, decisions, reviews = result

    typer.echo("\n--- Inference Run Summary ---")
    typer.echo(f"Run ID: {manifest.run_context.run_id}")
    typer.echo(f"Universe Size: {manifest.universe_size}")
    typer.echo("Action Class Distribution:")
    for cls_name, count in manifest.final_action_class_distribution.items():
        typer.echo(f"  - {cls_name}: {count}")

    if manifest.warnings:
        typer.echo("\nWarnings:")
        for w in manifest.warnings:
            typer.echo(f"  ! {w}")


@app.command(
    name="preview-artifact-chain",
    help="Preview the artifact resolution chain for a specific context",
)
def preview_artifact_chain(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    policy: str = typer.Option("latest_compatible", help="Resolution policy"),
):
    from sports_signal_bot.inference.resolver import ArtifactResolver

    resolver = ArtifactResolver()
    chain = resolver.resolve_chain(sport, market, policy=policy)

    typer.echo(f"\nArtifact Chain Resolution (Policy: {policy})")
    typer.echo(f"Valid: {chain.is_valid}")
    typer.echo(f"Model: {chain.model_artifact_id}")
    typer.echo(f"Calibrator: {chain.calibrator_artifact_id}")
    typer.echo(f"Ensemble: {chain.ensemble_artifact_id}")
    typer.echo(f"Stacker: {chain.stacker_artifact_id}")
    typer.echo(f"Threshold Policy: {chain.threshold_policy_id}")

    if chain.warnings:
        typer.echo("\nWarnings during resolution:")
        for w in chain.warnings:
            typer.echo(f"  - {w}")


@app.command(
    name="preview-event-universe", help="Preview the event universe for a specific slot"
)
def preview_event_universe(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    slot: str = typer.Option(..., help="Slot identifier"),
):
    from datetime import datetime

    from sports_signal_bot.inference.slots import SlotResolver
    from sports_signal_bot.inference.universe import EventUniverseBuilder

    resolver = SlotResolver()
    slot_def = resolver.resolve_slot_definition(slot)

    builder = EventUniverseBuilder()
    target_dt = datetime.utcnow()

    typer.echo(f"\nEvent Universe Preview (Slot: {slot_def.name})")
    typer.echo(f"Target Date: {target_dt.isoformat()}")
    typer.echo(f"Lookahead: {slot_def.lookahead_window_hours}h")

    raw = builder.build_event_universe(
        target_dt, sport, slot_def.lookahead_window_hours
    )
    filtered = builder.filter_supported_markets(raw, market)

    typer.echo(f"Found {len(filtered)} valid events for {sport} - {market}:")
    for e in filtered:
        typer.echo(
            f"  - [{e.event_id}] {e.home_team} vs {e.away_team} ({e.event_datetime_utc.isoformat()})"
        )


@app.command(
    name="preview-inference-packets", help="Preview decision packets structure"
)
def preview_inference_packets(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
):
    runner = InferenceRunner()
    result = runner.run(sport, market, slot_name="morning", mode="preview_mode")
    if result:
        _, decisions, _ = result
        for d in decisions:
            typer.echo(f"\nPacket: {d.event_id}")
            typer.echo(f"  Match: {d.teams}")
            typer.echo(f"  Signal Score: {d.signal_score:.2f}")
            typer.echo(f"  Action Class: {d.policy_action_class}")


@app.command(name="list-inference-slots", help="List available inference slots")
def list_inference_slots():
    from sports_signal_bot.inference.slots import SlotResolver

    resolver = SlotResolver()
    typer.echo("\nAvailable Inference Slots:")
    for slot_id, cfg in resolver.configs.items():
        typer.echo(
            f"  - {slot_id}: {cfg['name']} (Horizon: {cfg.get('event_inclusion_horizon_hours', 0)}h, Lookahead: {cfg.get('lookahead_window_hours', 12)}h)"
        )


if __name__ == "__main__":
    app()
