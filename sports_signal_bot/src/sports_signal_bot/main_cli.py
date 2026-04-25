import os
import uuid
from typing import List

import typer
import yaml

# Dummy imports to simulate classifiers registration
import sports_signal_bot.regimes.event
import sports_signal_bot.regimes.period
from sports_signal_bot.regimes import (RegimeConfig, RegimeFactory,
                                       RegimeRegistry, RegimeRunner,
                                       RegimeThresholdsConfig,
                                       build_event_regime_inputs,
                                       build_period_regime_inputs,
                                       build_regime_manifest,
                                       calculate_coverage,
                                       export_event_regimes_csv,
                                       export_period_regimes_csv,
                                       export_regime_manifest,
                                       generate_regime_summary)

# Assuming app is already defined in main.py, we will just patch it
app = typer.Typer(help="Sports Signal Bot CLI")


def _load_configs(sport: str):
    with open("configs/regimes/thresholds.yaml") as f:
        t_data = yaml.safe_load(f)
    t_config = RegimeThresholdsConfig(**t_data)

    with open(f"configs/regimes/{sport}.yaml") as f:
        r_data = yaml.safe_load(f)
    r_config = RegimeConfig(**r_data)

    return t_config, r_config


@app.command()
def list_regime_families():
    """Lists active regime families"""
    event_families = list(RegimeRegistry.get_event_classifiers().keys())
    period_families = list(RegimeRegistry.get_period_classifiers().keys())

    typer.echo("Active Event Regime Families:")
    for f in event_families:
        typer.echo(f"  - {f}")

    typer.echo("Active Period Regime Families:")
    for f in period_families:
        typer.echo(f"  - {f}")


@app.command()
def assign_regimes(sport: str = typer.Option(...), market: str = typer.Option(...)):
    """Assign regimes to events"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    # Mock data
    inputs = build_event_regime_inputs(
        event_id="evt_123",
        sport=sport,
        market_type=market,
        features={
            "home_form_score": 0.8,
            "away_form_score": 0.2,
            "home_rest_days": 2,
            "away_rest_days": 4,
        },
        ensemble_probabilities={"home": 0.7, "away": 0.3},
        source_probabilities={
            "bookie1": {"home": 0.75, "away": 0.25},
            "bookie2": {"home": 0.65, "away": 0.35},
        },
    )

    result = runner.assign_event_regimes(inputs)

    typer.echo(
        f"Assigned {len(result.event_regimes)} event regimes for {sport} {market}"
    )
    for r in result.event_regimes:
        typer.echo(
            f"  - {r.regime_family}: {r.regime_label} (method: {r.assignment_method})"
        )

    os.makedirs("results/regimes", exist_ok=True)
    export_event_regimes_csv(result.event_regimes, "results/regimes/event_regimes.csv")
    typer.echo("Saved to results/regimes/event_regimes.csv")


@app.command()
def preview_regime_coverage(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview regime coverage"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    # Mock multiple events
    records = []
    for i in range(150):  # Above min threshold
        inputs = build_event_regime_inputs(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            features={"home_form_score": 0.8, "away_form_score": 0.2},
            ensemble_probabilities={"home": 0.7, "away": 0.3},
        )
        res = runner.assign_event_regimes(inputs)
        records.extend(res.event_regimes)

    coverages = calculate_coverage(records, t_config)
    manifest = build_regime_manifest(
        run_id=str(uuid.uuid4()),
        active_families=r_config.enabled_regime_families,
        coverages=coverages,
        evaluations=[],
    )

    typer.echo(generate_regime_summary(manifest))

    os.makedirs("results/regimes", exist_ok=True)
    export_regime_manifest(manifest, "results/regimes/regime_manifest.json")
    typer.echo("Saved manifest to results/regimes/regime_manifest.json")


@app.command()
def preview_regime_leaderboard(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview leaderboard by regime"""
    typer.echo(f"Previewing regime leaderboard for {sport} {market}")
    typer.echo("Note: Real evaluation integration is mocked in this command.")
    typer.echo("  - Regime: market_disagreement: high_source_disagreement")
    typer.echo("    1. Source A (LogLoss: 0.65)")
    typer.echo("    2. Source B (LogLoss: 0.68)")


@app.command()
def preview_period_regimes(
    sport: str = typer.Option(...), market: str = typer.Option(...)
):
    """Preview period regimes"""
    t_config, r_config = _load_configs(sport)
    factory = RegimeFactory(t_config, r_config)
    runner = RegimeRunner(factory)

    inputs = build_period_regime_inputs(
        period_id=1,
        sport=sport,
        market_type=market,
        historical_metrics=[{"log_loss": 0.6}, {"log_loss": 0.65}],
    )
    result = runner.assign_period_regimes(inputs)

    typer.echo(f"Assigned period regimes for {sport} {market}")
    for r in result.period_regimes:
        typer.echo(f"  - {r.regime_family}: {r.regime_label}")

    os.makedirs("results/regimes", exist_ok=True)
    export_period_regimes_csv(
        result.period_regimes, "results/regimes/period_regimes.csv"
    )
    typer.echo("Saved to results/regimes/period_regimes.csv")


if __name__ == "__main__":
    app()
