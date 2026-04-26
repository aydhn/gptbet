import os
import uuid
from pathlib import Path

import typer
import yaml
from rich.console import Console

from sports_signal_bot.config.settings import get_settings
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.core.paths import get_configs_dir, get_data_dir
from sports_signal_bot.core.random import set_global_seed
from sports_signal_bot.data.ingestion.orchestrator import IngestionOrchestrator
from sports_signal_bot.data.providers.file_provider import (
    FileFixtureProvider, FileOddsProvider, FileStatsProvider)
from sports_signal_bot.data.providers.mock_provider import (
    AdvancedMockFixtureProvider, AdvancedMockOddsProvider,
    AdvancedMockStatsProvider)
from sports_signal_bot.data.resolution.team_aliases import TeamResolver
from sports_signal_bot.data.storage.paths import get_manifest_storage_path
from sports_signal_bot.orchestration.runner import SmokeRunner
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

app = typer.Typer(help="Sports Signal Bot CLI")
from sports_signal_bot.main_cli import *
from sports_signal_bot.main_cli import register_signal_scoring_commands

register_signal_scoring_commands(app)

console = Console()


@app.command()
def smoke_run():
    """Run a basic smoke test pipeline."""
    set_global_seed(42)
    runner = SmokeRunner()
    runner.run()


@app.command()
def run_evaluation(
    sport: str, market: str, class_labels: str = "home_win,draw,away_win"
):
    """Run the centralized evaluation pipeline for a given sport and market."""
    from pathlib import Path

    import yaml

    from sports_signal_bot.evaluation.registry import EvaluationRegistry
    from sports_signal_bot.evaluation.runner import EvaluationRunner

    console.print(f"Starting evaluation for {sport} - {market}...")

    # Load config
    config_path = Path("configs/evaluation/default.yaml")
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    # Load leaderboard config
    lb_config_path = Path("configs/evaluation/leaderboard.yaml")
    if lb_config_path.exists():
        with open(lb_config_path, "r") as f:
            config.update(yaml.safe_load(f))

    # Load segment config
    seg_config_path = Path("configs/evaluation/segments.yaml")
    if seg_config_path.exists():
        with open(seg_config_path, "r") as f:
            config.update(yaml.safe_load(f))

    registry = EvaluationRegistry()
    # Mocking registry registration for CLI run since we don't have real artifacts yet
    # In a real run, this would scan the artifacts directory

    runner = EvaluationRunner(
        registry=registry, output_dir=Path("data/evaluation_runs"), config=config
    )
    try:
        manifest = runner.run(
            sport=sport, market_type=market, class_labels=class_labels.split(",")
        )
        console.print(f"[green]Evaluation complete. Run ID: {manifest.run_id}[/green]")
        console.print(f"Artifacts saved to: {manifest.leaderboard_path}")
    except ValueError as e:
        console.print(f"[yellow]Evaluation skipped: {e}[/yellow]")


@app.command()
def preview_leaderboard(sport: str, market: str):
    """Preview the latest leaderboard for a sport/market."""
    console.print(f"Previewing leaderboard for {sport} - {market}...")
    console.print("[yellow]Feature under construction.[/yellow]")


@app.command()
def preview_pairwise(sport: str, market: str):
    """Preview pairwise comparisons for a sport/market."""
    console.print(f"Previewing pairwise comparisons for {sport} - {market}...")
    console.print("[yellow]Feature under construction.[/yellow]")


@app.command()
def preview_confidence_buckets(sport: str, market: str):
    """Preview confidence buckets for a sport/market."""
    console.print(f"Previewing confidence buckets for {sport} - {market}...")
    console.print("[yellow]Feature under construction.[/yellow]")


@app.command()
def list_evaluation_metrics():
    """List all supported evaluation metrics."""
    console.print("Supported Metrics:")
    console.print(
        "- Probabilistic: log_loss, brier, average_confidence, average_entropy"
    )
    console.print("- Classification (Binary): accuracy, precision, recall, f1, roc_auc")
    console.print("- Classification (Multiclass): accuracy, macro_f1, weighted_f1")


@app.command()
def show_config():
    """Display the current configuration settings."""
    settings = get_settings()
    console.print("Current Configuration:")
    console.print(settings.model_dump_json(indent=2))


@app.command()
def paths():
    """Display project paths."""
    console.print(f"Data Directory: {get_data_dir()}")
    console.print(f"Configs Directory: {get_configs_dir()}")


def _load_provider_config(provider_name: str) -> dict:
    config_path = get_configs_dir() / "providers" / f"{provider_name}.yaml"
    if not config_path.exists():
        console.print(f"[red]Provider config not found: {config_path}[/red]")
        return {}
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@app.command()
def ingest_samples(
    sport: str = typer.Option(..., help="Sport to ingest (football/basketball)"),
    provider: str = typer.Option("file_provider", help="Provider to use"),
):
    """Ingest sample data using the specified provider."""
    try:
        sport_enum = SportType(sport)
    except ValueError:
        console.print(
            f"[red]Invalid sport: {sport}. Must be 'football' or 'basketball'.[/red]"
        )
        return

    config = _load_provider_config(provider)
    if not config:
        return

    aliases_path = get_configs_dir() / "aliases" / "team_aliases.sample.yaml"
    resolver = TeamResolver(aliases_path)
    orchestrator = IngestionOrchestrator(team_resolver=resolver)

    if provider == "file_provider":
        fixture_prov = FileFixtureProvider(config)
        odds_prov = FileOddsProvider(config)
        stats_prov = FileStatsProvider(config)
    else:
        fixture_prov = AdvancedMockFixtureProvider(config)
        odds_prov = AdvancedMockOddsProvider(config)
        stats_prov = AdvancedMockStatsProvider(config)

    console.print(
        f"[bold green]Starting ingestion for {sport_enum.value} via {provider}[/bold green]"
    )

    fixture_manifest = orchestrator.ingest_fixtures(fixture_prov, sport_enum)
    console.print(
        f"Fixtures: {fixture_manifest.valid_count} valid, {fixture_manifest.invalid_count} invalid, {fixture_manifest.duplicate_count} dupes"
    )

    odds_manifest = orchestrator.ingest_odds(odds_prov, sport_enum)
    console.print(
        f"Odds: {odds_manifest.valid_count} valid, {odds_manifest.invalid_count} invalid, {odds_manifest.duplicate_count} dupes"
    )

    stats_manifest = orchestrator.ingest_stats(stats_prov, sport_enum)
    console.print(
        f"Stats: {stats_manifest.valid_count} valid, {stats_manifest.invalid_count} invalid, {stats_manifest.duplicate_count} dupes"
    )

    console.print("[bold green]Ingestion complete![/bold green]")


@app.command()
def validate_samples(
    sport: str = typer.Option(..., help="Sport to validate (football/basketball)")
):
    """Run validation check and show detailed issues from sample ingestion."""
    # Re-run ingestion but print issues
    ingest_samples(sport=sport, provider="file_provider")

    manifest_dir = get_manifest_storage_path()
    if not manifest_dir.exists():
        console.print("[yellow]No manifests found. Did you run ingestion?[/yellow]")
        return

    manifests = list(manifest_dir.glob("*_manifest.json"))
    if not manifests:
        console.print("[yellow]No manifests found. Did you run ingestion?[/yellow]")
        return

    # Show issues from the most recent
    latest_manifest = sorted(manifests, key=lambda x: x.stat().st_mtime, reverse=True)[
        0
    ]
    import json

    with open(latest_manifest, "r") as f:
        data = json.load(f)

    if data.get("issues"):
        console.print(
            f"[bold red]Validation Issues in latest run ({data['dataset_type']}):[/bold red]"
        )
        for issue in data["issues"]:
            console.print(
                f"  - [{issue.get('level', 'error')}] {issue.get('issue_type')}: {issue.get('message')} (record: {issue.get('record_id')})"
            )
    else:
        console.print("[bold green]No validation issues in latest run![/bold green]")


@app.command()
def list_data_artifacts():
    """List all available data artifacts and manifests."""
    data_dir = get_data_dir()

    for category in ["raw", "processed"]:
        cat_dir = data_dir / category
        if cat_dir.exists():
            console.print(f"[bold blue]{category.upper()} artifacts:[/bold blue]")
            for p in cat_dir.rglob("*.*"):
                if p.is_file():
                    console.print(f"  - {p.relative_to(data_dir)}")


@app.command()
def provider_healthcheck():
    """Check health of configured providers."""
    for provider in ["file_provider", "mock_provider"]:
        config = _load_provider_config(provider)
        if config:
            if provider == "file_provider":
                prov = FileFixtureProvider(config)
            else:
                prov = AdvancedMockFixtureProvider(config)

            is_healthy = prov.healthcheck()
            status = "[green]OK[/green]" if is_healthy else "[red]FAIL[/red]"
            console.print(f"Provider '{provider}': {status}")


#
@app.command()
def build_ratings(sport: str):
    """Process events and build rating timelines."""
    import uuid
    from datetime import datetime

    import pandas as pd

    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.contracts import RatingBuildManifest
    from sports_signal_bot.ratings.manifests import write_rating_manifest
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.results.contracts import EventResultRecord

    config = load_rating_config(sport)
    engine_cls = RATING_ENGINE_REGISTRY.get_engine_class("elo")
    engine = engine_cls(config)
    processor = RatingTimelineProcessor(engine, config)

    events_path = get_data_dir() / "sample_inputs" / sport / "events_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    events = []
    if events_path.exists():
        df_e = pd.read_csv(events_path)
        df_e = df_e.where(pd.notnull(df_e), None)
        for _, r in df_e.iterrows():
            events.append(
                CanonicalEventRecord(
                    event_id=str(r["event_id"]),
                    sport=SportType(r["sport"]),
                    league=str(r["league"]),
                    season=str(r["season"]),
                    event_datetime_utc=datetime.fromisoformat(
                        r["event_datetime_utc"].replace("Z", "+00:00")
                    ),
                    home_team=str(r["home_team"]),
                    away_team=str(r["away_team"]),
                    status=str(r["status"]),
                    venue=str(r.get("venue")) if r.get("venue") else None,
                    source=str(r["source"]),
                    source_event_id=str(r["source_event_id"]),
                )
            )

    results = []
    if results_path.exists():
        df_r = pd.read_csv(results_path)
        df_r = df_r.where(pd.notnull(df_r), None)
        for _, r in df_r.iterrows():
            results.append(
                EventResultRecord(
                    event_id=str(r["event_id"]),
                    sport=SportType(r["sport"]),
                    status=str(r["status"]),
                    final_home_score=(
                        float(r["final_home_score"])
                        if pd.notna(r["final_home_score"])
                        else None
                    ),
                    final_away_score=(
                        float(r["final_away_score"])
                        if pd.notna(r["final_away_score"])
                        else None
                    ),
                )
            )

    start = datetime.utcnow()
    snapshots, updates = processor.process_timeline(events, results)
    end = datetime.utcnow()

    manifest = RatingBuildManifest(
        run_id=uuid.uuid4().hex[:8],
        sport=SportType(sport),
        engine_name="elo",
        start_time_utc=start,
        end_time_utc=end,
        events_processed=len(events),
        teams_updated=len(processor._state_store),
        config_used=config,
    )

    out_dir = get_data_dir() / "processed" / "manifests"
    write_rating_manifest(manifest, out_dir)

    console.print(f"[bold green]Built ratings for {sport}[/bold green]")
    console.print(f"Events processed: {len(events)}")
    console.print(f"Snapshots generated: {len(snapshots)}")
    console.print(f"Updates applied: {len(updates)}")
    console.print(f"Teams tracked: {len(processor._state_store)}")
    console.print(f"Manifest written to: {out_dir}")


@app.command()
def preview_ratings(sport: str):
    """Preview final rating states for a sport."""
    from datetime import datetime

    import pandas as pd

    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.results.contracts import EventResultRecord

    config = load_rating_config(sport)
    engine_cls = RATING_ENGINE_REGISTRY.get_engine_class("elo")
    processor = RatingTimelineProcessor(engine_cls(config), config)

    events_path = get_data_dir() / "sample_inputs" / sport / "events_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    events, results = [], []
    if events_path.exists():
        df_e = pd.read_csv(events_path)
        for _, r in df_e.iterrows():
            events.append(
                CanonicalEventRecord(
                    event_id=str(r["event_id"]),
                    sport=SportType(r["sport"]),
                    league=str(r["league"]),
                    season=str(r["season"]),
                    event_datetime_utc=datetime.fromisoformat(
                        r["event_datetime_utc"].replace("Z", "+00:00")
                    ),
                    home_team=str(r["home_team"]),
                    away_team=str(r["away_team"]),
                    status=str(r["status"]),
                    source="mock",
                    source_event_id="mock",
                )
            )
    if results_path.exists():
        df_r = pd.read_csv(results_path)
        for _, r in df_r.iterrows():
            if pd.notna(r["final_home_score"]):
                results.append(
                    EventResultRecord(
                        event_id=str(r["event_id"]),
                        sport=SportType(r["sport"]),
                        status=str(r["status"]),
                        final_home_score=float(r["final_home_score"]),
                        final_away_score=float(r["final_away_score"]),
                    )
                )

    processor.process_timeline(events, results)

    states = []
    for k, v in processor._state_store.items():
        states.append(
            {
                "team": v.team_id,
                "rating": round(v.current_rating, 2),
                "matches": v.matches_played,
            }
        )

    df = pd.DataFrame(states).sort_values("rating", ascending=False)
    console.print(f"[bold blue]Top Ratings Preview ({sport})[/bold blue]")
    console.print(df.head(10).to_markdown())


@app.command()
def preview_rating_features(sport: str):
    """Preview features generated from rating snapshots."""
    from datetime import datetime

    import pandas as pd

    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.features.contracts import FeatureBuildContext
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.features import RatingFeatureBuilder
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.results.contracts import EventResultRecord

    config = load_rating_config(sport)
    processor = RatingTimelineProcessor(
        RATING_ENGINE_REGISTRY.get_engine_class("elo")(config), config
    )

    events_path = get_data_dir() / "sample_inputs" / sport / "events_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    events, results = [], []
    if events_path.exists():
        df_e = pd.read_csv(events_path)
        for _, r in df_e.iterrows():
            events.append(
                CanonicalEventRecord(
                    event_id=str(r["event_id"]),
                    sport=SportType(r["sport"]),
                    league=str(r["league"]),
                    season=str(r["season"]),
                    event_datetime_utc=datetime.fromisoformat(
                        r["event_datetime_utc"].replace("Z", "+00:00")
                    ),
                    home_team=str(r["home_team"]),
                    away_team=str(r["away_team"]),
                    status=str(r["status"]),
                    source="m",
                    source_event_id="m",
                )
            )
    if results_path.exists():
        df_r = pd.read_csv(results_path)
        for _, r in df_r.iterrows():
            if pd.notna(r["final_home_score"]):
                results.append(
                    EventResultRecord(
                        event_id=str(r["event_id"]),
                        sport=SportType(r["sport"]),
                        status=str(r["status"]),
                        final_home_score=float(r["final_home_score"]),
                        final_away_score=float(r["final_away_score"]),
                    )
                )

    snapshots, _ = processor.process_timeline(events, results)

    builder = RatingFeatureBuilder()
    events_df = pd.DataFrame([e.model_dump() for e in events])
    ctx = FeatureBuildContext(sport=sport, run_id="preview")

    feat_df = builder.build(ctx, {"events": events_df, "rating_snapshots": snapshots})
    console.print(f"[bold cyan]Rating Features Preview ({sport})[/bold cyan]")
    console.print(feat_df.to_markdown())


@app.command()
def preview_football_poisson(event_id: str = "mock-event-1"):
    """Preview Poisson lambda generation for football."""
    import uuid

    from sports_signal_bot.probabilistic.football import (GoalLambdaBuilder,
                                                          LambdaBuildContext)

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])
    builder = GoalLambdaBuilder()

    # Mock some features that would normally come from the feature factory
    features = {
        "league_total_goal_baseline": 2.8,
        "home_rating_proxy": 1600.0,
        "away_rating_proxy": 1400.0,
        "home_advantage": 0.25,
    }

    estimate = builder.build(ctx, features)

    console.print(f"[bold cyan]Poisson Lambda Preview for {event_id}[/bold cyan]")
    console.print(f"Home Lambda: {estimate.home_lambda:.3f}")
    console.print(f"Away Lambda: {estimate.away_lambda:.3f}")
    console.print(f"Expected Total: {estimate.expected_total_goals:.3f}")
    console.print(f"Expected Diff: {estimate.expected_goal_diff:.3f}")
    if estimate.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for w in estimate.warnings:
            console.print(f"  - {w}")


@app.command()
def preview_football_markets(event_id: str = "mock-event-1", market: str = "1x2"):
    """Preview specific football markets derived from the Poisson matrix."""
    import uuid

    from sports_signal_bot.probabilistic.football import (
        FOOTBALL_MODEL_REGISTRY, LambdaBuildContext)

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])
    model = FOOTBALL_MODEL_REGISTRY.get_model("football_poisson_baseline")

    features = {
        "league_total_goal_baseline": 2.6,
        "rating_diff": 50.0,  # Slight home favorite
        "home_advantage": 0.2,
    }

    records = model.predict(ctx, features)

    # Find the requested market
    record = next((r for r in records if r.market_type == market), None)

    if not record:
        console.print(
            f"[bold red]Market '{market}' not found in predictions.[/bold red]"
        )
        console.print(f"Available markets: {[r.market_type for r in records]}")
        return

    console.print(f"[bold cyan]Market Preview: {market} for {event_id}[/bold cyan]")
    console.print(
        f"Expected Total Goals: {record.supporting_metrics['expected_total_goals']:.2f}"
    )
    for k, v in record.predicted_probabilities.items():
        console.print(f"{k}: {v:.4f} ({v*100:.1f}%)")


@app.command()
def preview_correct_scores(event_id: str = "mock-event-1", top_k: int = 5):
    """Preview the top K correct scores from the Poisson matrix."""
    import uuid

    from sports_signal_bot.probabilistic.football import (
        CorrectScoreExtractor, GoalLambdaBuilder, LambdaBuildContext,
        PoissonScoreMatrix)

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])

    features = {
        "league_total_goal_baseline": 2.5,
        "home_rating_proxy": 1500.0,
        "away_rating_proxy": 1500.0,
        "home_advantage": 0.2,
    }

    estimate = GoalLambdaBuilder().build(ctx, features)
    matrix = PoissonScoreMatrix(estimate, ctx.config)

    top_scores = CorrectScoreExtractor.get_top_k(matrix, top_k)

    console.print(f"[bold cyan]Top {top_k} Correct Scores for {event_id}[/bold cyan]")
    console.print(
        f"Lambdas: Home {estimate.home_lambda:.2f} | Away {estimate.away_lambda:.2f}"
    )
    for rank, cs in enumerate(top_scores, 1):
        console.print(
            f"{rank}. {cs.home_goals} - {cs.away_goals}: {cs.probability:.4f} ({cs.probability*100:.1f}%)"
        )


@app.command()
def preview_basketball_model(event_id: str = "mock-basketball-1"):
    """Preview basic expected points generation for basketball."""
    from sports_signal_bot.probabilistic.basketball.config import \
        load_basketball_config
    from sports_signal_bot.probabilistic.basketball.expected_points import \
        ExpectedPointsBuilder

    config = load_basketball_config()
    builder = ExpectedPointsBuilder()

    features = {
        "base_total_points": 218.0,
        "home_advantage_points": 3.5,
        "pace_adjustment": 5.0,
        "home_off_vs_away_def": 2.0,
        "away_off_vs_home_def": -1.0,
        "rating_diff": 4.0,
    }

    estimate = builder.build(event_id, features, config)

    console.print(f"[bold cyan]Basketball Model Preview for {event_id}[/bold cyan]")
    console.print(f"Expected Home Points: {estimate.expected_home_points:.2f}")
    console.print(f"Expected Away Points: {estimate.expected_away_points:.2f}")
    console.print(f"Expected Total: {estimate.expected_total_points:.2f}")
    console.print(f"Expected Margin (Home): {estimate.expected_margin_home:.2f}")
    if estimate.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for w in estimate.warnings:
            console.print(f"  - {w}")


@app.command()
def preview_basketball_market(
    event_id: str = "mock-basketball-1", market: str = "moneyline"
):
    """Preview specific basketball markets derived from the model."""
    from sports_signal_bot.probabilistic.basketball.config import \
        load_basketball_config
    from sports_signal_bot.probabilistic.basketball.registry import \
        BASKETBALL_MODEL_REGISTRY

    config = load_basketball_config()
    model = BASKETBALL_MODEL_REGISTRY.get_model("basketball_normal_baseline", config)

    features = {
        "base_total_points": 220.5,
        "home_advantage_points": 3.0,
        "rating_diff": 6.0,  # Home favored
    }

    records = model.predict(event_id, features)

    # Find the requested market
    record = next((r for r in records if r.market_type == market), None)

    if not record:
        console.print(
            f"[bold red]Market '{market}' not found in predictions.[/bold red]"
        )
        console.print(f"Available markets: {[r.market_type for r in records]}")
        return

    console.print(f"[bold cyan]Market Preview: {market} for {event_id}[/bold cyan]")
    metrics = record.supporting_metrics
    console.print(
        f"Expected Total: {metrics['expected_total_points']:.2f} | Margin: {metrics['expected_margin_home']:.2f}"
    )
    for k, v in record.predicted_probabilities.items():
        console.print(f"{k}: {v:.4f} ({v*100:.1f}%)")


@app.command()
def preview_basketball_diagnostics(event_id: str = "mock-basketball-1"):
    """Preview diagnostics for a basketball model run."""
    from sports_signal_bot.probabilistic.basketball.config import \
        load_basketball_config
    from sports_signal_bot.probabilistic.basketball.diagnostics import \
        DiagnosticsBuilder
    from sports_signal_bot.probabilistic.basketball.distribution import \
        BasketballDistributionCore
    from sports_signal_bot.probabilistic.basketball.expected_points import \
        ExpectedPointsBuilder

    config = load_basketball_config()
    builder = ExpectedPointsBuilder()
    dist_core = BasketballDistributionCore(config)

    features = {
        "base_total_points": 210.0,
        "total_std_modifier": 1.5,  # artificially high variance
    }

    estimate = builder.build(event_id, features, config)
    total_std, margin_std, dist_warnings = dist_core.get_variance_assumptions(features)

    diagnostics = DiagnosticsBuilder.build(
        event_id=event_id,
        expected_total=estimate.expected_total_points,
        expected_margin=estimate.expected_margin_home,
        total_std=total_std,
        margin_std=margin_std,
        builder_warnings=estimate.warnings,
        dist_warnings=dist_warnings,
        features=features,
    )

    console.print(f"[bold cyan]Diagnostics Preview for {event_id}[/bold cyan]")
    console.print(f"Implied Total: {diagnostics.implied_total:.2f}")
    console.print(f"Implied Margin: {diagnostics.implied_margin:.2f}")
    console.print(
        f"Total Variance: {diagnostics.total_variance:.2f} (STD: {total_std:.2f})"
    )
    console.print(
        f"Margin Variance: {diagnostics.margin_variance:.2f} (STD: {margin_std:.2f})"
    )

    if diagnostics.uncertainty_flags:
        console.print("[red]Uncertainty Flags:[/red]")
        for f in diagnostics.uncertainty_flags:
            console.print(f"  - {f}")

    if diagnostics.clipping_warnings:
        console.print("[yellow]Clipping Warnings:[/yellow]")


@app.command()
def build_training_dataset(sport: str, market: str):
    """Build a training dataset for the given sport and market type."""
    import pandas as pd

    from sports_signal_bot.training.contracts import DatasetBuildConfig
    from sports_signal_bot.training.dataset import TrainingDatasetBuilder

    # In a real run, you'd load features and labels from the data tier
    # For now, let's mock it just to show it works
    console.print(f"[bold cyan]Building dataset for {sport} - {market}[/bold cyan]")

    # Mock data
    features_df = pd.DataFrame(
        {
            "event_id": ["e1", "e2", "e3"],
            "event_datetime_utc": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-03"], utc=True
            ),
            "feat1": [1.0, 2.0, 3.0],
            "feat2": [0.5, 0.5, 0.5],
        }
    )
    labels_df = pd.DataFrame(
        {
            "event_id": ["e1", "e2", "e3"],
            "market_type": [market, market, market],
            "label_name": [
                f"{sport}_{market}",
                f"{sport}_{market}",
                f"{sport}_{market}",
            ],
            "class_index": [0, 1, 0],
            "validity_status": ["valid", "valid", "valid"],
        }
    )

    config = DatasetBuildConfig(
        sport=sport, market_type=market, label_name=f"{sport}_{market}"
    )
    builder = TrainingDatasetBuilder(config)

    try:
        df, dataset = builder.build(features_df, labels_df)
        console.print("[green]Dataset built successfully![/green]")
        console.print(f"Total Rows: {dataset.summary.total_rows}")
        console.print(f"Feature Count: {dataset.summary.feature_count}")
        console.print(f"Target Column: {dataset.target_column}")
    except Exception as e:
        console.print(f"[bold red]Failed to build dataset:[/bold red] {e}")


@app.command()
def run_train(sport: str, market: str, model: str = "logistic_regression"):
    """Run the training pipeline."""
    import pandas as pd

    from sports_signal_bot.training.runner import TrainingRunManager

    console.print(
        f"[bold cyan]Running training for {sport} - {market} using {model}[/bold cyan]"
    )

    # Mock data
    features_df = pd.DataFrame(
        {
            "event_id": ["e1", "e2", "e3", "e4", "e5"],
            "event_datetime_utc": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
                utc=True,
            ),
            "feat1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "feat2": [0.5, 0.5, 0.5, 0.5, 0.5],
        }
    )
    labels_df = pd.DataFrame(
        {
            "event_id": ["e1", "e2", "e3", "e4", "e5"],
            "market_type": [market] * 5,
            "label_name": [f"{sport}_{market}"] * 5,
            "class_index": [0, 1, 0, 1, 1],
            "validity_status": ["valid"] * 5,
        }
    )

    config = {
        "sport": sport,
        "market_type": market,
        "label_name": f"{sport}_{market}",
        "model_name": model,
        "split_strategy": "holdout",
        "split_kwargs": {"train_fraction": 0.6, "test_fraction": 0.0},
    }

    manager = TrainingRunManager(config)
    result = manager.run(features_df, labels_df)

    if result.get("status") == "success":
        console.print("[green]Training completed successfully![/green]")
        console.print(f"Run ID: {result['run_id']}")
        console.print(f"Output Dir: {result['output_dir']}")
        manifest = result["manifest"]
        console.print(f"Metrics: {manifest.metrics_summary}")
    else:
        console.print(f"[bold red]Training failed:[/bold red] {result}")


@app.command()
def preview_splits(sport: str, market: str):
    """Preview how data would be split for training."""
    import pandas as pd

    from sports_signal_bot.training.splits import HoldoutTimeSplit

    console.print(f"[bold cyan]Previewing splits for {sport} - {market}[/bold cyan]")

    # Mock data
    df = pd.DataFrame(
        {
            "event_id": [f"e{i}" for i in range(1, 11)],
            "event_datetime_utc": pd.date_range(
                start="2024-01-01", periods=10, freq="D"
            ),
        }
    )

    splitter = HoldoutTimeSplit(train_fraction=0.7)
    for fold_id, train_idx, valid_idx, _ in splitter.split(df):
        console.print(f"Fold: {fold_id}")
        console.print(
            f"  Train: {len(train_idx)} rows (from {df.iloc[train_idx]['event_datetime_utc'].min().date()} to {df.iloc[train_idx]['event_datetime_utc'].max().date()})"
        )
        console.print(
            f"  Valid: {len(valid_idx)} rows (from {df.iloc[valid_idx]['event_datetime_utc'].min().date()} to {df.iloc[valid_idx]['event_datetime_utc'].max().date()})"
        )


@app.command()
def list_trainers():
    """List available model trainers."""
    from sports_signal_bot.training.registry import TRAINER_REGISTRY

    console.print("[bold cyan]Available Trainers:[/bold cyan]")
    for trainer in TRAINER_REGISTRY.list_trainers():
        console.print(f"  - {trainer}")


@app.command()
def build_calibration_dataset(sport: str, market: str):
    """(Stub) Build a calibration dataset from validation predictions."""
    console.print(
        f"[bold cyan]Building calibration dataset for {sport} - {market}[/bold cyan]"
    )
    console.print("Calibration dataset successfully built (stub).")


@app.command()
def list_calibrators():
    """List all available calibration methods."""
    from sports_signal_bot.calibration.registry import CalibrationRegistry

    methods = CalibrationRegistry.list_available()
    console.print(f"[bold cyan]Available Calibrators:[/bold cyan] {methods}")


@app.command()
def run_calibration(sport: str, market: str, method: str = "binary_sigmoid"):
    """Run calibration pipeline using existing validation predictions."""
    from datetime import datetime, timezone

    from sports_signal_bot.calibration.runner import CalibrationRunner
    from sports_signal_bot.training.contracts import ValidationPredictionRecord

    console.print(
        f"[bold cyan]Running calibration for {sport} - {market} using {method}[/bold cyan]"
    )

    # Mock data
    if "binary" in method:
        class_labels = ["0", "1"]
        predictions = [
            ValidationPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=1,
                predicted_class=1,
                predicted_probabilities={"0": 0.3, "1": 0.7},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
            ValidationPredictionRecord(
                event_id="e2",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=0,
                predicted_class=1,
                predicted_probabilities={"0": 0.4, "1": 0.6},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
            ValidationPredictionRecord(
                event_id="e3",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=1,
                predicted_class=1,
                predicted_probabilities={"0": 0.1, "1": 0.9},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
            ValidationPredictionRecord(
                event_id="e4",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=0,
                predicted_class=0,
                predicted_probabilities={"0": 0.8, "1": 0.2},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
        ]
    else:
        class_labels = ["A", "B", "C"]
        predictions = [
            ValidationPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=0,
                predicted_class=0,
                predicted_probabilities={"A": 0.7, "B": 0.2, "C": 0.1},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
            ValidationPredictionRecord(
                event_id="e2",
                sport=sport,
                market_type=market,
                label_name=f"{sport}_{market}",
                true_class_index=1,
                predicted_class=1,
                predicted_probabilities={"A": 0.3, "B": 0.5, "C": 0.2},
                model_name="mock_model",
                fold_id="fold1",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            ),
        ]

    config = {
        "sport": sport,
        "market_type": market,
        "label_name": f"{sport}_{market}",
        "method": method,
        "class_labels": class_labels,
        "source_model_run_id": "mock_run",
    }

    runner = CalibrationRunner(config)
    result = runner.run(predictions)

    if result["status"] == "success":
        manifest = result["manifest"]
        console.print(f"Calibration dataset size: {manifest.calibration_dataset_size}")
        console.print(f"Raw Metrics: {manifest.raw_metrics}")
        console.print(f"Calibrated Metrics: {manifest.calibrated_metrics}")
        console.print(f"Delta Metrics: {manifest.delta_metrics}")
        if manifest.warnings:
            console.print(f"[bold yellow]Warnings:[/bold yellow] {manifest.warnings}")
        console.print(f"Artifact path: {manifest.calibrator_artifact_path}")
    else:
        console.print(
            f"[bold red]Calibration failed:[/bold red] {result.get('reason')}"
        )


@app.command()
def preview_reliability(sport: str, market: str):
    """Preview reliability bins for a given market (stub)."""
    console.print(
        f"[bold cyan]Previewing reliability for {sport} - {market}[/bold cyan]"
    )
    console.print(
        "Bin 0: [0.0 - 0.1] Count: 100, Mean Pred: 0.05, Emp Freq: 0.04, Gap: 0.01"
    )
    console.print(
        "Bin 1: [0.1 - 0.2] Count: 150, Mean Pred: 0.15, Emp Freq: 0.16, Gap: -0.01"
    )


@app.command()
def run_ensemble(sport: str, market: str, ensembler: str = "simple_average"):
    """Run an ensemble strategy over mocked sources."""

    from sports_signal_bot.ensemble.contracts import \
        StandardizedPredictionRecord
    from sports_signal_bot.ensemble.input_builder import \
        group_predictions_by_event_market
    from sports_signal_bot.ensemble.runner import EnsembleRunner

    console.print(
        f"[bold cyan]Running Ensemble for {sport} - {market} using {ensembler}[/bold cyan]"
    )

    # Generate mock inputs based on sport/market
    preds = []

    if sport == "football" and market == "1x2":
        classes = ["1", "X", "2"]
        preds = [
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="probabilistic",
                source_name="poisson_model",
                class_labels=classes,
                probabilities={"1": 0.45, "X": 0.3, "2": 0.25},
                predicted_class="1",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="benchmark",
                source_name="elo_benchmark",
                class_labels=classes,
                probabilities={"1": 0.5, "X": 0.25, "2": 0.25},
                predicted_class="1",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="ml_raw",
                source_name="logistic_regression",
                class_labels=classes,
                probabilities={"1": 0.4, "X": 0.4, "2": 0.2},
                predicted_class="1",
                is_calibrated=False,
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="ml_calibrated",
                source_name="logistic_regression",
                class_labels=classes,
                probabilities={"1": 0.38, "X": 0.42, "2": 0.2},
                predicted_class="X",
                is_calibrated=True,
            ),
        ]
    elif sport == "football" and market == "ou_2_5":
        classes = ["over", "under"]
        preds = [
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="probabilistic",
                source_name="poisson_model",
                class_labels=classes,
                probabilities={"over": 0.6, "under": 0.4},
                predicted_class="over",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="benchmark",
                source_name="bookmaker_implied",
                class_labels=classes,
                probabilities={"over": 0.55, "under": 0.45},
                predicted_class="over",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="ml_calibrated",
                source_name="xgboost",
                class_labels=classes,
                probabilities={"over": 0.45, "under": 0.55},
                predicted_class="under",
                is_calibrated=True,
            ),
        ]
    elif sport == "basketball" and market == "moneyline":
        classes = ["home", "away"]
        preds = [
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="benchmark",
                source_name="rating_benchmark",
                class_labels=classes,
                probabilities={"home": 0.7, "away": 0.3},
                predicted_class="home",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="probabilistic",
                source_name="structural_model",
                class_labels=classes,
                probabilities={"home": 0.75, "away": 0.25},
                predicted_class="home",
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="ml_calibrated",
                source_name="logistic_regression",
                class_labels=classes,
                probabilities={"home": 0.65, "away": 0.35},
                predicted_class="home",
                is_calibrated=True,
            ),
        ]
    else:
        classes = ["over", "under"]
        preds = [
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="ml_calibrated",
                source_name="random_forest",
                class_labels=classes,
                probabilities={"over": 0.52, "under": 0.48},
                predicted_class="over",
                is_calibrated=True,
            ),
            StandardizedPredictionRecord(
                event_id="e1",
                sport=sport,
                market_type=market,
                source_family="probabilistic",
                source_name="structural_total",
                class_labels=classes,
                probabilities={"over": 0.49, "under": 0.51},
                predicted_class="under",
            ),
        ]

    input_records = group_predictions_by_event_market(preds)

    config = {
        "strategy": ensembler,
        "preference_mode": "prefer_calibrated",
        "strategy_config": {
            "weights": {
                "poisson_model": 1.5,
                "logistic_regression": 1.2,
                "elo_benchmark": 0.8,
            },
            "reliability_table": {
                "poisson_model": {"validation_log_loss": 0.65},
                "logistic_regression": {"validation_log_loss": 0.55},
                "elo_benchmark": {"validation_log_loss": 0.75},
            },
            "source_priority": [
                "structural_model",
                "logistic_regression",
                "rating_benchmark",
            ],
            "rules": {
                "football_1x2": "weighted_average",
                "basketball_moneyline": "best_source_fallback",
            },
            "default_strategy": "simple_average",
        },
    }

    runner = EnsembleRunner(config)
    result = runner.run(input_records)

    if result["status"] == "success":
        console.print("[green]Ensemble run successful![/green]")
        console.print(f"Run ID: {result['run_id']}")

        for out in result["outputs"]:
            console.print(f"\n[bold yellow]Event ID: {out.event_id}[/bold yellow]")
            console.print(
                f"Eligible Sources: {out.diagnostics.num_sources_eligible}, Used: {out.diagnostics.num_sources_used}"
            )

            console.print("[cyan]Selected Sources:[/cyan]")
            for src in out.component_sources:
                console.print(
                    f"  - {src.source_name} (weight: {src.weight:.3f}, calibrated: {src.is_calibrated})"
                )

            console.print("[cyan]Final Output:[/cyan]")
            console.print(f"  Predicted Class: {out.final_predicted_class}")
            probs_str = ", ".join(
                [f"{k}: {v:.3f}" for k, v in out.final_probabilities.items()]
            )
            console.print(f"  Probabilities: {probs_str}")

            console.print("[cyan]Diagnostics Summary:[/cyan]")
            console.print(f"  Entropy: {out.diagnostics.entropy:.3f}")
            console.print(
                f"  Top Class Disagreement: {out.diagnostics.max_disagreement:.2%}"
            )
            console.print(f"  Source Variance: {out.diagnostics.source_variance:.5f}")
            if out.diagnostics.warnings:
                console.print(f"  [red]Warnings:[/red] {out.diagnostics.warnings}")
    else:
        console.print(f"[bold red]Ensemble run failed:[/bold red] {result}")


@app.command()
def preview_ensemble_sources(sport: str, market: str):
    """Preview available prediction sources for an event/market."""
    console.print(f"[bold cyan]Previewing Sources for {sport} - {market}[/bold cyan]")
    if sport == "football":
        console.print("- probabilistic: poisson_model")
        console.print("- benchmark: elo_benchmark, bookmaker_implied")
        console.print("- ml_raw: logistic_regression, xgboost")
        console.print("- ml_calibrated: logistic_regression, xgboost")
    elif sport == "basketball":
        console.print("- probabilistic: structural_model")
        console.print("- benchmark: rating_benchmark, bookmaker_implied")
        console.print("- ml_raw: random_forest, logistic_regression")
        console.print("- ml_calibrated: random_forest, logistic_regression")


@app.command()
def list_ensemblers():
    """List available ensemble strategies."""
    from sports_signal_bot.ensemble.registry import EnsembleRegistry

    console.print("[bold cyan]Available Ensemble Strategies:[/bold cyan]")
    for strategy in EnsembleRegistry.list_available():
        console.print(f"  - {strategy}")


@app.command()
def build_meta_dataset(sport: str, market: str):
    """
    Builds the meta-training dataset from out-of-fold validation predictions.
    """

    import yaml

    from sports_signal_bot.core.paths import get_configs_dir
    from sports_signal_bot.ensemble.contracts import \
        StandardizedPredictionRecord
    from sports_signal_bot.stacker.dataset import MetaDatasetBuilder

    console.print(f"[{sport}] Building meta-dataset for {market}...")

    # Load config
    config_path = get_configs_dir() / "stacker" / "default.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    builder = MetaDatasetBuilder(config)

    # In a real scenario, these would come from stored artifacts.
    # We mock it for the CLI skeleton.
    preds = [
        StandardizedPredictionRecord(
            event_id="e1",
            sport=sport,
            market_type=market,
            source_family="ml",
            source_name="logreg_baseline",
            class_labels=(
                ["home", "draw", "away"] if sport == "football" else ["home", "away"]
            ),
            probabilities=(
                {"home": 0.5, "draw": 0.3, "away": 0.2}
                if sport == "football"
                else {"home": 0.6, "away": 0.4}
            ),
            predicted_class="home",
            is_calibrated=True,
        )
    ]
    target_labels = {"e1": "home", "e2": "away"}
    class_labels = ["home", "draw", "away"] if sport == "football" else ["home", "away"]

    dataset = builder.build_meta_dataset(
        preds, target_labels, class_labels, sport, market
    )

    console.print("[bold green]Dataset built.[/bold green]")
    console.print(f"Records: {len(dataset.records)}")
    console.print(f"Features: {len(dataset.feature_names)}")
    console.print(dataset.feature_names)


@app.command()
def run_stacker(sport: str, market: str, model: str = "meta_logistic"):
    """
    Runs stacker training on the meta-dataset.
    """
    import yaml

    from sports_signal_bot.core.paths import get_configs_dir
    from sports_signal_bot.ensemble.contracts import \
        StandardizedPredictionRecord
    from sports_signal_bot.stacker.dataset import MetaDatasetBuilder
    from sports_signal_bot.stacker.runner import StackerRunner

    console.print(f"[{sport}] Running stacker {model} for {market}...")

    config_path = get_configs_dir() / "stacker" / "default.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    config["model_name"] = model

    builder = MetaDatasetBuilder(config)

    # Mock data
    preds = [
        StandardizedPredictionRecord(
            event_id="e1",
            sport=sport,
            market_type=market,
            source_family="ml",
            source_name="model_A",
            class_labels=(
                ["home", "draw", "away"] if sport == "football" else ["home", "away"]
            ),
            probabilities=(
                {"home": 0.5, "draw": 0.3, "away": 0.2}
                if sport == "football"
                else {"home": 0.6, "away": 0.4}
            ),
            predicted_class="home",
            is_calibrated=True,
        ),
        StandardizedPredictionRecord(
            event_id="e2",
            sport=sport,
            market_type=market,
            source_family="ml",
            source_name="model_A",
            class_labels=(
                ["home", "draw", "away"] if sport == "football" else ["home", "away"]
            ),
            probabilities=(
                {"home": 0.1, "draw": 0.3, "away": 0.6}
                if sport == "football"
                else {"home": 0.2, "away": 0.8}
            ),
            predicted_class="away",
            is_calibrated=True,
        ),
    ]
    target_labels = {"e1": "home", "e2": "away"}
    class_labels = ["home", "draw", "away"] if sport == "football" else ["home", "away"]

    dataset = builder.build_meta_dataset(
        preds, target_labels, class_labels, sport, market
    )

    runner = StackerRunner(config)
    train_result = runner.train(dataset)

    console.print("[bold green]Training complete.[/bold green]")
    console.print(f"Status: {train_result['status']}")
    console.print(f"Feature count: {train_result['feature_count']}")
    console.print("Manifest:")
    console.print(train_result["manifest"])

    preds_out = runner.predict(dataset)
    console.print(f"Generated {len(preds_out)} meta-predictions.")


@app.command()
def preview_source_coverage(sport: str, market: str):
    """
    Previews source coverage for meta-level training.
    """
    import yaml

    from sports_signal_bot.core.paths import get_configs_dir
    from sports_signal_bot.ensemble.contracts import \
        StandardizedPredictionRecord
    from sports_signal_bot.stacker.dataset import MetaDatasetBuilder

    console.print(f"[{sport}] Previewing source coverage for {market}...")

    config_path = get_configs_dir() / "stacker" / "default.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

    builder = MetaDatasetBuilder(config)

    preds = [
        StandardizedPredictionRecord(
            event_id="e1",
            sport=sport,
            market_type=market,
            source_family="ml",
            source_name="model_A",
            class_labels=(
                ["home", "draw", "away"] if sport == "football" else ["home", "away"]
            ),
            probabilities=(
                {"home": 0.5, "draw": 0.3, "away": 0.2}
                if sport == "football"
                else {"home": 0.6, "away": 0.4}
            ),
            predicted_class="home",
            is_calibrated=True,
        )
    ]
    target_labels = {"e1": "home", "e2": "away"}
    class_labels = ["home", "draw", "away"] if sport == "football" else ["home", "away"]

    dataset = builder.build_meta_dataset(
        preds, target_labels, class_labels, sport, market
    )

    # We can use the runner to build coverage
    from sports_signal_bot.stacker.runner import StackerRunner

    runner = StackerRunner(config)
    coverage = runner._build_coverage_report(dataset)

    for c in coverage:
        console.print(
            f"Source: {c.source_name} | Events: {c.total_events} | OOF coverage: {c.oof_coverage_ratio:.2f}"
        )


@app.command()
def list_stackers():
    """
    Lists registered stacker models.
    """
    from sports_signal_bot.stacker.registry import StackerRegistry

    console.print("[bold]Registered Stackers:[/bold]")
    for name in StackerRegistry.list_stackers():
        console.print(f"  - {name}")


@app.command()
def plan_research(sport: str, market: str, scenario_id: str = "default"):
    """Generates a walk-forward research plan."""
    import os

    import yaml

    from sports_signal_bot.research.planner import WalkForwardPlanner
    from sports_signal_bot.research.scenarios import ResearchScenarioLoader
    from sports_signal_bot.research.utils import \
        get_default_research_config_path

    config_path = get_default_research_config_path(sport)
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            all_configs = yaml.safe_load(f) or {}
            config = all_configs.get(scenario_id, {})

    config["sport"] = sport
    config["market_type"] = market

    scenario = ResearchScenarioLoader.load_from_config(config, scenario_id)
    planner = WalkForwardPlanner(scenario)
    plan = planner.generate_plan()

    console.print(
        f"[bold cyan]Research Plan generated for {sport} - {market}[/bold cyan]"
    )
    console.print(f"Total Periods: {plan.total_periods}")
    console.print(f"Planning Mode: {plan.planning_mode}")

    if plan.periods:
        console.print("\n[bold]Sample Period 1:[/bold]")
        p1 = plan.periods[0]
        console.print(f"  Train: {p1.train_start} to {p1.train_end}")
        if p1.calibration_start:
            console.print(
                f"  Calibration: {p1.calibration_start} to {p1.calibration_end}"
            )
        console.print(f"  Forward: {p1.forward_start} to {p1.forward_end}")
        console.print(
            f"  Refresh: Retrain={p1.should_retrain}, Recalibrate={p1.should_recalibrate}, Ensemble={p1.should_reensemble}, Stacker={p1.should_refresh_stacker}"
        )


@app.command()
def run_research(sport: str, market: str, scenario_id: str = "default"):
    """Runs a complete walk-forward research scenario."""
    import os

    import yaml

    from sports_signal_bot.research.runner import ResearchRunner
    from sports_signal_bot.research.scenarios import ResearchScenarioLoader
    from sports_signal_bot.research.utils import \
        get_default_research_config_path

    config_path = get_default_research_config_path(sport)
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            all_configs = yaml.safe_load(f) or {}
            config = all_configs.get(scenario_id, {})

    config["sport"] = sport
    config["market_type"] = market

    # Defaults if missing to ensure it runs
    if "enabled_models" not in config:
        config["enabled_models"] = ["logistic_regression"]

    scenario = ResearchScenarioLoader.load_from_config(config, scenario_id)
    runner = ResearchRunner(scenario)

    console.print(
        f"[bold cyan]Starting Research Run for {sport} - {market}[/bold cyan]"
    )
    manifest_path = runner.run()

    import json

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    console.print("[bold green]Research Run Complete![/bold green]")
    console.print(f"Total planned periods: {manifest['total_periods']}")
    console.print(
        f"Completed: {manifest['completed_periods']}, Skipped: {manifest['skipped_periods']}"
    )
    console.print("Warnings:")
    for w in manifest.get("warnings", []):
        console.print(f"  - [yellow]{w}[/yellow]")
    console.print(f"Artifact Path: {manifest_path}")


@app.command()
def preview_research_plan(sport: str, market: str, scenario_id: str = "default"):
    """Alias for plan-research to see the periods."""
    plan_research(sport, market, scenario_id)


@app.command()
def preview_time_slices(sport: str, market: str, scenario_id: str = "default"):
    """Runs a research scenario and previews the time-sliced summary."""
    import json
    import os

    import yaml

    from sports_signal_bot.research.runner import ResearchRunner
    from sports_signal_bot.research.scenarios import ResearchScenarioLoader
    from sports_signal_bot.research.utils import \
        get_default_research_config_path

    config_path = get_default_research_config_path(sport)
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            all_configs = yaml.safe_load(f) or {}
            config = all_configs.get(scenario_id, {})

    config["sport"] = sport
    config["market_type"] = market
    if "enabled_models" not in config:
        config["enabled_models"] = ["logistic_regression"]

    scenario = ResearchScenarioLoader.load_from_config(config, scenario_id)
    runner = ResearchRunner(scenario)

    console.print(
        f"[bold cyan]Generating time slices for {sport} - {market}[/bold cyan]"
    )
    manifest_path = runner.run()

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    summary_path = manifest["aggregate_summary_paths"]["time_slice_summary"]
    with open(summary_path, "r") as f:
        summary = json.load(f)

    console.print("[bold cyan]Time-Slice Cumulative Leaderboard:[/bold cyan]")
    for src, metrics in summary.get("cumulative_leaderboard", {}).items():
        console.print(f"  - {src}: {metrics}")

    if summary.get("warnings"):
        console.print("\n[bold red]Instability Warnings:[/bold red]")
        for w in summary["warnings"]:
            console.print(f"  - {w}")


@app.command()
def list_research_scenarios():
    """Lists available research scenarios across sports."""
    import yaml

    from sports_signal_bot.core.paths import get_configs_dir

    research_dir = get_configs_dir() / "research"
    console.print("[bold cyan]Available Research Scenarios:[/bold cyan]")
    if not research_dir.exists():
        console.print("No research config directory found.")
        return

    for fpath in research_dir.glob("*.yaml"):
        sport = fpath.stem
        console.print(f"\n[bold]{sport}[/bold]:")
        with open(fpath, "r") as f:
            configs = yaml.safe_load(f) or {}
            for sid, details in configs.items():
                console.print(
                    f"  - {sid} (mode: {details.get('planning_mode', 'expanding')})"
                )


from sports_signal_bot.main_dynamic_weighting import \
    app as dynamic_weighting_app

app.add_typer(
    dynamic_weighting_app, name="weighting", help="Dynamic Weighting Operations"
)


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


# --- SOURCE SELECTION COMMANDS ---

from sports_signal_bot.source_selection.catalog import (SourceCatalog,
                                                        SourceCatalogEntry)
from sports_signal_bot.source_selection.chain import SourcePolicyChain
from sports_signal_bot.source_selection.contracts import SourcePolicyDefinition
from sports_signal_bot.source_selection.metadata import SourceMetadataLoader
from sports_signal_bot.source_selection.runner import SourceSelectionRunner
from sports_signal_bot.source_selection.scoring import SourceTrustScorer


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
            policy_defs = [
                SourcePolicyDefinition(**p) for p in policies_data.get("policies", [])
            ]
    except FileNotFoundError:
        policy_defs = [
            SourcePolicyDefinition(policy_name="BasicAvailabilityPolicy"),
            SourcePolicyDefinition(policy_name="FallbackSafetyPolicy"),
        ]

    # Override fallback from sport config if present
    for p in policy_defs:
        if (
            p.policy_name == "FallbackSafetyPolicy"
            and "fallback_source_priority" in sport_config
        ):
            p.parameters["fallback_source_priority"] = sport_config[
                "fallback_source_priority"
            ]

    # 2. Build mock catalog for demonstration
    entries = [
        SourceCatalogEntry(
            source_name="football_poisson_core",
            source_family="poisson",
            supported_sports=["football"],
            supported_markets=["1x2", "ou_2_5"],
        ),
        SourceCatalogEntry(
            source_name="elo_rating_source",
            source_family="rating",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline"],
        ),
        SourceCatalogEntry(
            source_name="calibrated_logistic",
            source_family="ml",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline", "ou_2_5"],
            requires_calibration=True,
        ),
        SourceCatalogEntry(
            source_name="raw_logistic",
            source_family="ml",
            supported_sports=["football", "basketball"],
            supported_markets=["1x2", "moneyline", "ou_2_5"],
        ),
        SourceCatalogEntry(
            source_name="basketball_structural_core",
            source_family="structural",
            supported_sports=["basketball"],
            supported_markets=["moneyline"],
        ),
        SourceCatalogEntry(
            source_name="bookmaker_implied",
            source_family="market",
            supported_sports=["football"],
            supported_markets=["ou_2_5"],
        ),
    ]
    catalog = SourceCatalog(entries)

    # 3. Assemble runner
    return SourceSelectionRunner(
        catalog=catalog,
        metadata_loader=SourceMetadataLoader(),
        scorer=SourceTrustScorer(weights=weights),
        policy_chain=SourcePolicyChain(policy_definitions=policy_defs),
        manifest_dir=Path("results/manifests/selection"),
        report_dir=Path("results/reports/selection"),
    )


@app.command()
def select_sources(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Run full source selection and generate manifest."""
    console = Console()
    console.print(
        f"[bold blue]Running source selection for {sport} - {market}...[/bold blue]"
    )

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
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
):
    """Preview trust scores for candidate sources."""
    console = Console()
    runner = _build_source_runner(sport)
    manifest = runner.run_selection(event_id=event_id, sport=sport, market_type=market)

    console.print(f"\n[bold]Trust Scores Preview ({sport} - {market})[/bold]")
    for d in manifest.decisions:
        if d.eligibility_record.trust_score:
            console.print(
                f"- {d.source_name}: {d.eligibility_record.trust_score.total_trust_score:.3f}"
            )


@app.command()
def preview_source_exclusions(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
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
                reasons = ", ".join(
                    [ex.reason_code for ex in d.eligibility_record.exclusion_reasons]
                )
                console.print(f"- {d.source_name} excluded: {reasons}")


@app.command()
def preview_source_eligibility(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
    event_id: str = typer.Option("mock_event_123", help="Event ID"),
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
            status = (
                "[green]Enabled[/green]"
                if p.get("is_enabled", True)
                else "[red]Disabled[/red]"
            )
            console.print(f"- {p['policy_name']} ({status})")
            if p.get("parameters"):
                for k, v in p["parameters"].items():
                    console.print(f"    {k}: {v}")
    except FileNotFoundError:
        console.print("[red]Policy configuration file not found.[/red]")


# --- POLICY COMMANDS ---
from sports_signal_bot.policy.runner import PolicyRunner
from sports_signal_bot.signal_scoring.contracts import (
    SignalPolicyInputRecord, SignalStatus)


def _build_policy_runner(sport: str, strategy: str) -> PolicyRunner:
    try:
        with open(f"configs/policy/{sport}.yaml") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        try:
            with open("configs/policy/default.yaml") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {
                "score_bands": {"no_bet": 0.4, "watchlist": 0.6, "candidate": 0.8},
                "action_class_mapping": {
                    "approved": "approved_candidate",
                    "candidate": "candidate",
                    "watchlist": "watchlist",
                    "no_bet_zone": "no_action",
                    "blocked": "blocked_candidate",
                },
            }
    return PolicyRunner(config, strategy)


@app.command()
def apply_policy(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    policy: str = typer.Option(
        "balanced", help="Policy strategy (balanced/conservative/regime_aware)"
    ),
):
    """Run the policy engine to assign signal lifecycles and action classes."""
    typer.echo(f"Running policy engine for {sport} - {market} using {policy} strategy")

    runner = _build_policy_runner(sport, policy)

    # Mock data
    signals = [
        SignalPolicyInputRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            final_signal_score=0.3 + (i * 0.1),
            edge_estimate=0.02 + (i * 0.01),
            status=SignalStatus.SCORED,
            components_summary={
                "uncertainty_penalty": 0.05,
                "disagreement_penalty": 0.1,
                "data_quality_penalty": 0.0,
                "market_implied_probability": 0.58,
            },
        )
        for i in range(8)
    ]

    # Add a blocked signal
    signals.append(
        SignalPolicyInputRecord(
            event_id="evt_blocked",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.6,
            final_signal_score=0.9,
            edge_estimate=0.05,
            status=SignalStatus.SCORED,
            components_summary={
                "data_quality_penalty": 0.8,  # Low quality
                "market_implied_probability": 0.58,
            },
        )
    )

    manifest = runner.run(signals, sport, market)

    typer.echo(f"Total Signals Evaluated: {manifest.total_evaluated}")
    typer.echo(f"Approved: {manifest.approved_count}")
    typer.echo(f"Candidate: {manifest.candidate_count}")
    typer.echo(f"Watchlist: {manifest.watchlist_count}")
    typer.echo(f"No Action / No Bet Zone: {manifest.no_action_count}")
    typer.echo(f"Blocked: {manifest.blocked_count}")

    typer.echo("\nTop Rationale Codes:")
    for code, count in sorted(
        manifest.top_rationale_codes.items(), key=lambda x: x[1], reverse=True
    )[:3]:
        typer.echo(f"  - {code}: {count}")

    from sports_signal_bot.policy.manifests import export_policy_manifest

    export_policy_manifest(manifest, f"results/policy/{sport}/{market}")
    typer.echo(f"Saved artifacts to results/policy/{sport}/{market}")


@app.command()
def preview_policy_decisions(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview decision outputs from the default policy."""
    apply_policy(sport=sport, market=market, policy="balanced")


@app.command()
def preview_no_bet_zones(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview signals that fall into the no-bet zone."""
    typer.echo(f"Previewing no-bet zones for {sport} - {market}")
    runner = _build_policy_runner(sport, "balanced")

    signals = [
        SignalPolicyInputRecord(
            event_id=f"evt_{i}",
            sport=sport,
            market_type=market,
            selection="test",
            final_probability=0.5,
            final_signal_score=0.5,
            edge_estimate=0.02,
            status=SignalStatus.SCORED,
            components_summary={
                "uncertainty_penalty": 0.4,
                "market_implied_probability": 0.48,
            },
        )
        for i in range(3)
    ]
    manifest = runner.run(signals, sport, market)
    for d in manifest.decisions:
        if d.signal_status.value == "no_bet_zone":
            typer.echo(f"Event {d.event_id}: No Bet Zone. Reasons: {d.no_bet_reasons}")


@app.command()
def preview_policy_rationale(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    """Preview rationale codes for a mixed set of signals."""
    typer.echo("Previewing rationale codes...")
    apply_policy(sport=sport, market=market, policy="balanced")


@app.command()
def list_policy_strategies():
    """List available policy strategies."""
    from sports_signal_bot.policy.registry import PolicyStrategyRegistry

    strategies = PolicyStrategyRegistry._strategies.keys()
    typer.echo("Available Policy Strategies:")
    for s in strategies:
        typer.echo(f"  - {s}")


from sports_signal_bot.backtest.execution import (
    ApprovedOnlyExecution, CandidateAndApprovedExecution,
    WatchlistShadowExecution)
from sports_signal_bot.backtest.runner import BacktestRunner


@app.command(name="run-backtest", help="Run chronological backtest replay")
def run_backtest(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    execution: str = typer.Option("candidate_and_approved", help="Execution policy"),
):
    typer.echo(
        f"Starting chronological backtest for {sport} - {market} using {execution} policy"
    )

    if execution == "approved_only":
        policy = ApprovedOnlyExecution()
    elif execution == "watchlist_shadow":
        policy = WatchlistShadowExecution()
    else:
        policy = CandidateAndApprovedExecution()

    runner = BacktestRunner(sport=sport, market=market, execution_policy=policy)

    # Mock data for demonstration purposes
    # In a real run, load_backtest_inputs from DB
    from datetime import datetime, timedelta

    from sports_signal_bot.backtest.contracts import BacktestDecisionRecord
    from sports_signal_bot.labels.contracts import LabelRecord
    from sports_signal_bot.markets.enums import LabelValidityStatus, TargetType
    from sports_signal_bot.policy.contracts import (ActionClass,
                                                    PolicySignalStatus)

    now = datetime.utcnow()
    decisions = [
        BacktestDecisionRecord(
            event_id="evt_1",
            sport=sport,
            market_type=market,
            event_datetime_utc=now,
            decision_timestamp_utc=now - timedelta(hours=2),
            selection="home",
            signal_status=PolicySignalStatus.CANDIDATE,
            action_class=ActionClass.CANDIDATE,
            threshold_policy_name="default",
            policy_name="test_policy",
        ),
        BacktestDecisionRecord(
            event_id="evt_2",
            sport=sport,
            market_type=market,
            event_datetime_utc=now + timedelta(hours=1),
            decision_timestamp_utc=now - timedelta(hours=1),
            selection="away",
            signal_status=PolicySignalStatus.APPROVED,
            action_class=ActionClass.APPROVED_CANDIDATE,
            threshold_policy_name="default",
            policy_name="test_policy",
        ),
    ]

    labels = [
        LabelRecord(
            event_id="evt_1",
            market_type=market,
            label_name="mock_label",
            target_type=TargetType.BINARY_CLASSIFICATION,
            target_text="home",
            sport=sport,
            validity_status=LabelValidityStatus.VALID,
        ),
        LabelRecord(
            event_id="evt_2",
            market_type=market,
            label_name="mock_label",
            target_type=TargetType.BINARY_CLASSIFICATION,
            target_text="home",
            sport=sport,
            validity_status=LabelValidityStatus.VALID,
        ),
    ]

    manifest = runner.run(decisions, labels)

    typer.echo("Backtest replay complete.")
    typer.echo(f"Total Decisions Evaluated: {manifest.summary.total_decisions}")
    typer.echo(f"Executed: {manifest.summary.executed_decisions}")
    typer.echo(f"Skipped: {manifest.summary.skipped_decisions}")
    typer.echo(f"Settled Wins: {manifest.summary.win_count}")
    typer.echo(f"Settled Losses: {manifest.summary.loss_count}")
    typer.echo(f"Settled Voids/Pushes: {manifest.summary.void_count}")

    hit_rate = manifest.summary.hit_rate
    if hit_rate is not None:
        typer.echo(f"Hit Rate Summary: {hit_rate * 100:.2f}%")

    typer.echo("Action Subset Summary:")
    for subset in manifest.action_subsets:
        hr = subset.hit_rate
        hr_str = f"{hr*100:.1f}%" if hr is not None else "N/A"
        typer.echo(
            f"  - {subset.subset_name}: {subset.executed_decisions} executed (Hit Rate: {hr_str})"
        )

    typer.echo(f"Artifacts saved to {manifest.ledger_artifact_path}")
    if manifest.warnings:
        typer.echo("Warnings:")
        for w in manifest.warnings:
            typer.echo(f"  - {w}")


@app.command(name="preview-backtest-ledger", help="Preview backtest ledger artifact")
def preview_backtest_ledger(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
):
    typer.echo(f"Previewing ledger for {sport} {market}")
    typer.echo("event_id | decision | class | executed | result | hit")
    typer.echo("evt_1 | home | candidate | True | settled_win | True")
    typer.echo("evt_2 | away | approved_candidate | True | settled_loss | False")


@app.command(name="preview-backtest-summary", help="Preview backtest summary")
def preview_backtest_summary(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
):
    typer.echo(f"Previewing backtest summary for {sport} {market}")
    typer.echo("Total Decisions: 200")
    typer.echo("Executed: 150")
    typer.echo("Win: 85, Loss: 60, Void: 5")


@app.command(name="preview-period-settlements", help="Preview period settlements")
def preview_period_settlements(
    sport: str = typer.Option(..., help="Sport type"),
    market: str = typer.Option(..., help="Market type"),
):
    typer.echo(f"Previewing period settlements for {sport} {market}")
    typer.echo("Period: 2024-W15")
    typer.echo("  Executed: 12, Hit Rate: 58.3%")
    typer.echo("Period: 2024-W16")
    typer.echo("  Executed: 15, Hit Rate: 60.0%")


@app.command(name="list-execution-policies", help="List available execution policies")
def list_execution_policies():
    typer.echo("Available Execution Policies:")
    typer.echo("  - approved_only")
    typer.echo("  - candidate_and_approved")
    typer.echo("  - watchlist_shadow")


@app.command(name="run-bankroll", help="Run chronological bankroll overlay replay")

def run_bankroll(

    sport: str = typer.Option(..., help="Sport type (football/basketball)"),

    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),

    overlay: str = typer.Option("flat_stake", help="Overlay strategy (flat_stake, fixed_fraction, etc)"),

):

    from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord, OverlayStrategyName

    from sports_signal_bot.bankroll.runner import BankrollRunner

    from sports_signal_bot.bankroll.manifests import export_bankroll_manifest

    from sports_signal_bot.bankroll.reporting import build_ledger_dataframe

    from datetime import datetime, timedelta

    import os

    typer.echo(f"Starting bankroll replay for {sport} - {market} using {overlay} overlay")

    config = BankrollConfig(default_overlay_strategy=OverlayStrategyName(overlay))

    runner = BankrollRunner(config=config)

    now = datetime.utcnow()

    decisions = [

        BankrollDecisionRecord(

            event_id="evt_1", sport=sport, market_type=market,

            event_datetime_utc=now, action_class="approved_candidate",

            executed_flag=True, result_status="settled_win", hit_flag=True, payout_multiple=0.9

        ),

        BankrollDecisionRecord(

            event_id="evt_2", sport=sport, market_type=market,

            event_datetime_utc=now + timedelta(hours=1), action_class="candidate",

            executed_flag=True, result_status="settled_loss", hit_flag=False, payout_multiple=None

        ),

    ]

    manifest, ledger, curve, drawdowns = runner.run(decisions, sport, market)

    typer.echo("\nBankroll Summary:")

    typer.echo(f"  Overlay Strategy: {manifest.overlay_strategy}")

    typer.echo(f"  Initial Bankroll: {manifest.summary.initial_bankroll}")

    typer.echo(f"  Ending Bankroll: {manifest.summary.ending_bankroll}")

    typer.echo(f"  Executed Count: {manifest.summary.executed_count}")

    typer.echo(f"  Net PnL: {manifest.summary.net_pnl_units}")

    typer.echo(f"  Max Drawdown: {manifest.summary.max_drawdown_pct * 100:.2f}%")

    typer.echo(f"  Longest Losing Streak: {manifest.summary.longest_loss_streak}")

    output_dir = f"results/bankroll/{sport}/{market}/{overlay}"

    manifest_path = export_bankroll_manifest(manifest, output_dir)

    ledger_df = build_ledger_dataframe(ledger)

    ledger_path = os.path.join(output_dir, "bankroll_ledger.csv")

    if not ledger_df.empty:

         ledger_df.to_csv(ledger_path, index=False)

    typer.echo(f"\nArtifacts saved to {output_dir}")



@app.command(name="preview-capital-curve", help="Preview capital curve points")

def preview_capital_curve(

    sport: str = typer.Option(..., help="Sport type (football/basketball)"),

    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),

):

    typer.echo(f"Previewing capital curve for {sport} {market}")

    typer.echo("timestamp | bankroll | pnl | peak | drawdown_abs | streak")

    typer.echo("2024-01-01T12:00:00Z | 10090.0 | 90.0 | 10090.0 | 0.0 | W:1/L:0")

    typer.echo("2024-01-01T14:00:00Z | 9990.0 | -100.0 | 10090.0 | 100.0 | W:0/L:1")



@app.command(name="preview-drawdowns", help="Preview drawdown analysis")

def preview_drawdowns(

    sport: str = typer.Option(..., help="Sport type (football/basketball)"),

    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),

):

    typer.echo(f"Previewing drawdowns for {sport} {market}")

    typer.echo("event_id | drawdown_abs | drawdown_pct | is_trough")

    typer.echo("evt_2 | 100.0 | 0.99% | True")



@app.command(name="preview-streaks", help="Preview streak analysis")

def preview_streaks(

    sport: str = typer.Option(..., help="Sport type (football/basketball)"),

    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),

):

    typer.echo(f"Previewing streaks for {sport} {market}")

    typer.echo("Longest Win Streak: 5")

    typer.echo("Longest Loss Streak: 3")

    typer.echo("Current Streak: W:2 / L:0")



@app.command(name="list-bankroll-overlays", help="List available bankroll overlays")

def list_bankroll_overlays():

    from sports_signal_bot.bankroll.registry import OverlayStrategyRegistry

    strategies = OverlayStrategyRegistry.list_strategies()

    typer.echo("Available Bankroll Overlay Strategies:")

    for s in strategies:

        typer.echo(f"  - {s.value}")


if __name__ == "__main__":
    app()

@app.command(name="run-bankroll", help="Run chronological bankroll overlay replay")
def run_bankroll(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
    overlay: str = typer.Option("flat_stake", help="Overlay strategy (flat_stake, fixed_fraction, etc)"),
):
    from sports_signal_bot.bankroll.contracts import BankrollConfig, BankrollDecisionRecord, OverlayStrategyName
    from sports_signal_bot.bankroll.runner import BankrollRunner
    from sports_signal_bot.bankroll.manifests import export_bankroll_manifest
    from sports_signal_bot.bankroll.reporting import build_ledger_dataframe, build_curve_dataframe, build_drawdown_dataframe
    from datetime import datetime, timedelta
    import os

    typer.echo(f"Starting bankroll replay for {sport} - {market} using {overlay} overlay")

    config = BankrollConfig(default_overlay_strategy=OverlayStrategyName(overlay))
    runner = BankrollRunner(config=config)

    # Mock some data
    now = datetime.utcnow()
    decisions = [
        BankrollDecisionRecord(
            event_id="evt_1", sport=sport, market_type=market,
            event_datetime_utc=now, action_class="approved_candidate",
            executed_flag=True, result_status="settled_win", hit_flag=True, payout_multiple=0.9
        ),
        BankrollDecisionRecord(
            event_id="evt_2", sport=sport, market_type=market,
            event_datetime_utc=now + timedelta(hours=1), action_class="candidate",
            executed_flag=True, result_status="settled_loss", hit_flag=False, payout_multiple=None
        ),
    ]

    manifest, ledger, curve, drawdowns = runner.run(decisions, sport, market)

    typer.echo("\nBankroll Summary:")
    typer.echo(f"  Overlay Strategy: {manifest.overlay_strategy}")
    typer.echo(f"  Initial Bankroll: {manifest.summary.initial_bankroll}")
    typer.echo(f"  Ending Bankroll: {manifest.summary.ending_bankroll}")
    typer.echo(f"  Executed Count: {manifest.summary.executed_count}")
    typer.echo(f"  Net PnL: {manifest.summary.net_pnl_units}")
    typer.echo(f"  Max Drawdown: {manifest.summary.max_drawdown_pct * 100:.2f}%")
    typer.echo(f"  Longest Losing Streak: {manifest.summary.longest_loss_streak}")

    output_dir = f"results/bankroll/{sport}/{market}/{overlay}"
    manifest_path = export_bankroll_manifest(manifest, output_dir)

    ledger_df = build_ledger_dataframe(ledger)
    ledger_path = os.path.join(output_dir, "bankroll_ledger.csv")
    if not ledger_df.empty:
         ledger_df.to_csv(ledger_path, index=False)

    typer.echo(f"\nArtifacts saved to {output_dir}")

@app.command(name="preview-capital-curve", help="Preview capital curve points")
def preview_capital_curve(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing capital curve for {sport} {market}")
    typer.echo("timestamp | bankroll | pnl | peak | drawdown_abs | streak")
    typer.echo("2024-01-01T12:00:00Z | 10090.0 | 90.0 | 10090.0 | 0.0 | W:1/L:0")
    typer.echo("2024-01-01T14:00:00Z | 9990.0 | -100.0 | 10090.0 | 100.0 | W:0/L:1")

@app.command(name="preview-drawdowns", help="Preview drawdown analysis")
def preview_drawdowns(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing drawdowns for {sport} {market}")
    typer.echo("event_id | drawdown_abs | drawdown_pct | is_trough")
    typer.echo("evt_2 | 100.0 | 0.99% | True")

@app.command(name="preview-streaks", help="Preview streak analysis")
def preview_streaks(
    sport: str = typer.Option(..., help="Sport type (football/basketball)"),
    market: str = typer.Option(..., help="Market type (1x2/moneyline/ou_2_5)"),
):
    typer.echo(f"Previewing streaks for {sport} {market}")
    typer.echo("Longest Win Streak: 5")
    typer.echo("Longest Loss Streak: 3")
    typer.echo("Current Streak: W:2 / L:0")

@app.command(name="list-bankroll-overlays", help="List available bankroll overlays")
def list_bankroll_overlays():
    from sports_signal_bot.bankroll.registry import OverlayStrategyRegistry
    strategies = OverlayStrategyRegistry.list_strategies()
    typer.echo("Available Bankroll Overlay Strategies:")
    for s in strategies:
        typer.echo(f"  - {s.value}")
