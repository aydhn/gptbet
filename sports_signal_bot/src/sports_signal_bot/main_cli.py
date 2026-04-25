import os
import uuid

import typer
import yaml

# Dummy imports to simulate classifiers registration
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

# --- SOURCE SELECTION COMMANDS ---

from sports_signal_bot.source_selection.contracts import SourcePolicyDefinition
from sports_signal_bot.source_selection.catalog import SourceCatalog, SourceCatalogEntry
from sports_signal_bot.source_selection.metadata import SourceMetadataLoader
from sports_signal_bot.source_selection.scoring import SourceTrustScorer
from sports_signal_bot.source_selection.chain import SourcePolicyChain
from sports_signal_bot.source_selection.runner import SourceSelectionRunner
from pathlib import Path
from rich.console import Console

def _build_source_runner(sport: str) -> SourceSelectionRunner:
    # 1. Load config
    try:
        with open(f"configs/source_selection/{sport}.yaml") as f:
            sport_config = yaml.safe_load(f)
    except FileNotFoundError:
        sport_config = {}

    try:
        with open("configs/source_selection/trust_weights.yaml") as f:
            weights = yaml.safe_load(f)
    except FileNotFoundError:
        weights = None

    try:
        with open("configs/source_selection/policies.yaml") as f:
            policies_data = yaml.safe_load(f)
            policy_defs = [SourcePolicyDefinition(**p) for p in policies_data.get("policies", [])]
    except FileNotFoundError:
        policy_defs = [
            SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy"),
            SourcePolicyDefinition(policy_name="FallbackSafetyPolicy")
        ]

    # Override fallback from sport config if present
    for p in policy_defs:
        if p.policy_name == "FallbackSafetyPolicy" and "fallback_source_priority" in sport_config:
            p.parameters["fallback_source_priority"] = sport_config["fallback_source_priority"]

    # 2. Build mock catalog for demonstration
    entries = [
        SourceCatalogEntry(source_name="football_poisson_core", source_family="poisson", supported_sports=["football"], supported_markets=["1x2", "ou_2_5"]),
        SourceCatalogEntry(source_name="elo_rating_source", source_family="rating", supported_sports=["football", "basketball"], supported_markets=["1x2", "moneyline"]),
        SourceCatalogEntry(source_name="calibrated_logistic", source_family="ml", supported_sports=["football", "basketball"], supported_markets=["1x2", "moneyline", "ou_2_5"], requires_calibration=True),
        SourceCatalogEntry(source_name="raw_logistic", source_family="ml", supported_sports=["football", "basketball"], supported_markets=["1x2", "moneyline", "ou_2_5"]),
        SourceCatalogEntry(source_name="basketball_structural_core", source_family="structural", supported_sports=["basketball"], supported_markets=["moneyline"]),
        SourceCatalogEntry(source_name="bookmaker_implied", source_family="market", supported_sports=["football"], supported_markets=["ou_2_5"])
    ]
    catalog = SourceCatalog(entries)

    # 3. Assemble runner
    return SourceSelectionRunner(
        catalog=catalog,
        metadata_loader=SourceMetadataLoader(),
        scorer=SourceTrustScorer(weights=weights),
        policy_chain=SourcePolicyChain(policy_definitions=policy_defs),
        manifest_dir=Path("results/manifests/selection"),
        report_dir=Path("results/reports/selection")
    )

@app.command()
def select_sources(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    event_id: str = typer.Option("mock_event_123", help="Event ID")
):
    """Run full source selection and generate manifest."""
    console = Console()
    console.print(f"[bold blue]Running source selection for {sport} - {market}...[/bold blue]")

    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print("[green]Selection complete![/green]")
    console.print(f"Candidates evaluated: {manifest.summary.total_candidates}")
    console.print(f"Eligible sources: {manifest.summary.eligible_count}")
    console.print(f"Selected: {', '.join(manifest.selected_sources)}")
    console.print(f"Fallback used: {manifest.summary.fallback_used}")
    console.print(f"Manifest written to results/manifests/selection/{manifest.run_id}")

@app.command()
def preview_source_trust(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID")
):
    """Preview trust scores for candidate sources."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Trust Scores Preview ({sport} - {market})[/bold]")
    for d in manifest.decisions:
        if d.eligibility_record.trust_score:
            console.print(f"- {d.source_name}: {d.eligibility_record.trust_score.total_trust_score:.3f}")

@app.command()
def preview_source_exclusions(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID")
):
    """Preview exclusion reasons for an event."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Exclusions Preview ({sport} - {market})[/bold]")
    if manifest.summary.excluded_count == 0:
        console.print("No sources were excluded.")
    else:
        for d in manifest.decisions:
            if not d.is_selected:
                reasons = ", ".join([ex.reason_code for ex in d.eligibility_record.exclusion_reasons])
                console.print(f"- {d.source_name} excluded: {reasons}")

@app.command()
def preview_source_eligibility(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID")
):
    """Preview final eligibility status of sources."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Eligibility Preview ({sport} - {market})[/bold]")
    for d in manifest.decisions:
        status = "[green]ELIGIBLE[/green]" if d.is_selected else "[red]EXCLUDED[/red]"
        console.print(f"{status} - {d.source_name}")

@app.command()
def list_source_policies():
    """List currently configured eligibility policies."""
    console = Console()
    try:
        with open("configs/source_selection/policies.yaml") as f:
            policies_data = yaml.safe_load(f)

        console.print("\n[bold]Configured Source Policies:[/bold]")
        for p in policies_data.get("policies", []):
            status = "[green]Enabled[/green]" if p.get("is_enabled", True) else "[red]Disabled[/red]"
            console.print(f"- {p['policy_name']} ({status})")
            if p.get("parameters"):
                for k, v in p["parameters"].items():
                    console.print(f"    {k}: {v}")
    except FileNotFoundError:
        console.print("[red]Policy configuration file not found.[/red]")
