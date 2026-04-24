import typer
from rich.console import Console
from pathlib import Path
import yaml

from sports_signal_bot.orchestration.runner import SmokeRunner
from sports_signal_bot.config.settings import get_settings
from sports_signal_bot.core.paths import get_data_dir, get_configs_dir
from sports_signal_bot.core.random import set_global_seed
from sports_signal_bot.core.constants import SportType

from sports_signal_bot.data.providers.file_provider import FileFixtureProvider, FileOddsProvider, FileStatsProvider
from sports_signal_bot.data.providers.mock_provider import AdvancedMockFixtureProvider, AdvancedMockOddsProvider, AdvancedMockStatsProvider
from sports_signal_bot.data.ingestion.orchestrator import IngestionOrchestrator
from sports_signal_bot.data.resolution.team_aliases import TeamResolver
from sports_signal_bot.data.storage.paths import get_manifest_storage_path

app = typer.Typer(help="Sports Signal Bot CLI")
console = Console()

@app.command()
def smoke_run():
    """Run a basic smoke test pipeline."""
    set_global_seed(42)
    runner = SmokeRunner()
    runner.run()

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
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@app.command()
def ingest_samples(sport: str = typer.Option(..., help="Sport to ingest (football/basketball)"), provider: str = typer.Option("file_provider", help="Provider to use")):
    """Ingest sample data using the specified provider."""
    try:
        sport_enum = SportType(sport)
    except ValueError:
        console.print(f"[red]Invalid sport: {sport}. Must be 'football' or 'basketball'.[/red]")
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

    console.print(f"[bold green]Starting ingestion for {sport_enum.value} via {provider}[/bold green]")

    fixture_manifest = orchestrator.ingest_fixtures(fixture_prov, sport_enum)
    console.print(f"Fixtures: {fixture_manifest.valid_count} valid, {fixture_manifest.invalid_count} invalid, {fixture_manifest.duplicate_count} dupes")

    odds_manifest = orchestrator.ingest_odds(odds_prov, sport_enum)
    console.print(f"Odds: {odds_manifest.valid_count} valid, {odds_manifest.invalid_count} invalid, {odds_manifest.duplicate_count} dupes")

    stats_manifest = orchestrator.ingest_stats(stats_prov, sport_enum)
    console.print(f"Stats: {stats_manifest.valid_count} valid, {stats_manifest.invalid_count} invalid, {stats_manifest.duplicate_count} dupes")

    console.print("[bold green]Ingestion complete![/bold green]")

@app.command()
def validate_samples(sport: str = typer.Option(..., help="Sport to validate (football/basketball)")):
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
    latest_manifest = sorted(manifests, key=lambda x: x.stat().st_mtime, reverse=True)[0]
    import json
    with open(latest_manifest, 'r') as f:
        data = json.load(f)

    if data.get('issues'):
        console.print(f"[bold red]Validation Issues in latest run ({data['dataset_type']}):[/bold red]")
        for issue in data['issues']:
            console.print(f"  - [{issue.get('level', 'error')}] {issue.get('issue_type')}: {issue.get('message')} (record: {issue.get('record_id')})")
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
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.ratings.manifests import write_rating_manifest
    from sports_signal_bot.ratings.contracts import RatingBuildManifest
    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.results.contracts import EventResultRecord
    import pandas as pd
    from datetime import datetime
    import uuid

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
            events.append(CanonicalEventRecord(
                event_id=str(r['event_id']),
                sport=SportType(r['sport']),
                league=str(r['league']),
                season=str(r['season']),
                event_datetime_utc=datetime.fromisoformat(r['event_datetime_utc'].replace('Z', '+00:00')),
                home_team=str(r['home_team']),
                away_team=str(r['away_team']),
                status=str(r['status']),
                venue=str(r.get('venue')) if r.get('venue') else None,
                source=str(r['source']),
                source_event_id=str(r['source_event_id'])
            ))

    results = []
    if results_path.exists():
        df_r = pd.read_csv(results_path)
        df_r = df_r.where(pd.notnull(df_r), None)
        for _, r in df_r.iterrows():
             results.append(EventResultRecord(
                 event_id=str(r['event_id']),
                 sport=SportType(r['sport']),
                 status=str(r['status']),
                 final_home_score=float(r['final_home_score']) if pd.notna(r['final_home_score']) else None,
                 final_away_score=float(r['final_away_score']) if pd.notna(r['final_away_score']) else None
             ))

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
        config_used=config
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
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.results.contracts import EventResultRecord
    import pandas as pd
    from datetime import datetime

    config = load_rating_config(sport)
    engine_cls = RATING_ENGINE_REGISTRY.get_engine_class("elo")
    processor = RatingTimelineProcessor(engine_cls(config), config)

    events_path = get_data_dir() / "sample_inputs" / sport / "events_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    events, results = [], []
    if events_path.exists():
        df_e = pd.read_csv(events_path)
        for _, r in df_e.iterrows():
            events.append(CanonicalEventRecord(
                event_id=str(r['event_id']), sport=SportType(r['sport']), league=str(r['league']), season=str(r['season']),
                event_datetime_utc=datetime.fromisoformat(r['event_datetime_utc'].replace('Z', '+00:00')),
                home_team=str(r['home_team']), away_team=str(r['away_team']), status=str(r['status']), source="mock", source_event_id="mock"
            ))
    if results_path.exists():
        df_r = pd.read_csv(results_path)
        for _, r in df_r.iterrows():
            if pd.notna(r['final_home_score']):
                 results.append(EventResultRecord(event_id=str(r['event_id']), sport=SportType(r['sport']), status=str(r['status']), final_home_score=float(r['final_home_score']), final_away_score=float(r['final_away_score'])))

    processor.process_timeline(events, results)

    states = []
    for k, v in processor._state_store.items():
        states.append({"team": v.team_id, "rating": round(v.current_rating, 2), "matches": v.matches_played})

    df = pd.DataFrame(states).sort_values('rating', ascending=False)
    console.print(f"[bold blue]Top Ratings Preview ({sport})[/bold blue]")
    console.print(df.head(10).to_markdown())

@app.command()
def preview_rating_features(sport: str):
    """Preview features generated from rating snapshots."""
    from sports_signal_bot.ratings.config import load_rating_config
    from sports_signal_bot.ratings.registry import RATING_ENGINE_REGISTRY
    from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
    from sports_signal_bot.ratings.features import RatingFeatureBuilder
    from sports_signal_bot.features.contracts import FeatureBuildContext
    from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
    from sports_signal_bot.results.contracts import EventResultRecord
    import pandas as pd
    from datetime import datetime

    config = load_rating_config(sport)
    processor = RatingTimelineProcessor(RATING_ENGINE_REGISTRY.get_engine_class("elo")(config), config)

    events_path = get_data_dir() / "sample_inputs" / sport / "events_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    events, results = [], []
    if events_path.exists():
        df_e = pd.read_csv(events_path)
        for _, r in df_e.iterrows():
            events.append(CanonicalEventRecord(
                event_id=str(r['event_id']), sport=SportType(r['sport']), league=str(r['league']), season=str(r['season']),
                event_datetime_utc=datetime.fromisoformat(r['event_datetime_utc'].replace('Z', '+00:00')),
                home_team=str(r['home_team']), away_team=str(r['away_team']), status=str(r['status']), source="m", source_event_id="m"
            ))
    if results_path.exists():
         df_r = pd.read_csv(results_path)
         for _, r in df_r.iterrows():
            if pd.notna(r['final_home_score']):
                 results.append(EventResultRecord(event_id=str(r['event_id']), sport=SportType(r['sport']), status=str(r['status']), final_home_score=float(r['final_home_score']), final_away_score=float(r['final_away_score'])))

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
    from sports_signal_bot.probabilistic.football import LambdaBuildContext, GoalLambdaBuilder
    import uuid

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])
    builder = GoalLambdaBuilder()

    # Mock some features that would normally come from the feature factory
    features = {
        "league_total_goal_baseline": 2.8,
        "home_rating_proxy": 1600.0,
        "away_rating_proxy": 1400.0,
        "home_advantage": 0.25
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
    from sports_signal_bot.probabilistic.football import LambdaBuildContext, FOOTBALL_MODEL_REGISTRY
    import uuid

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])
    model = FOOTBALL_MODEL_REGISTRY.get_model("football_poisson_baseline")

    features = {
        "league_total_goal_baseline": 2.6,
        "rating_diff": 50.0, # Slight home favorite
        "home_advantage": 0.2
    }

    records = model.predict(ctx, features)

    # Find the requested market
    record = next((r for r in records if r.market_type == market), None)

    if not record:
        console.print(f"[bold red]Market '{market}' not found in predictions.[/bold red]")
        console.print(f"Available markets: {[r.market_type for r in records]}")
        return

    console.print(f"[bold cyan]Market Preview: {market} for {event_id}[/bold cyan]")
    console.print(f"Expected Total Goals: {record.supporting_metrics['expected_total_goals']:.2f}")
    for k, v in record.predicted_probabilities.items():
        console.print(f"{k}: {v:.4f} ({v*100:.1f}%)")

@app.command()
def preview_correct_scores(event_id: str = "mock-event-1", top_k: int = 5):
    """Preview the top K correct scores from the Poisson matrix."""
    from sports_signal_bot.probabilistic.football import LambdaBuildContext, GoalLambdaBuilder, PoissonScoreMatrix, CorrectScoreExtractor
    import uuid

    ctx = LambdaBuildContext(event_id=event_id, run_id=uuid.uuid4().hex[:8])

    features = {
        "league_total_goal_baseline": 2.5,
        "home_rating_proxy": 1500.0,
        "away_rating_proxy": 1500.0,
        "home_advantage": 0.2
    }

    estimate = GoalLambdaBuilder().build(ctx, features)
    matrix = PoissonScoreMatrix(estimate, ctx.config)

    top_scores = CorrectScoreExtractor.get_top_k(matrix, top_k)

    console.print(f"[bold cyan]Top {top_k} Correct Scores for {event_id}[/bold cyan]")
    console.print(f"Lambdas: Home {estimate.home_lambda:.2f} | Away {estimate.away_lambda:.2f}")
    for rank, cs in enumerate(top_scores, 1):
        console.print(f"{rank}. {cs.home_goals} - {cs.away_goals}: {cs.probability:.4f} ({cs.probability*100:.1f}%)")


@app.command()
def preview_basketball_model(event_id: str = "mock-basketball-1"):
    """Preview basic expected points generation for basketball."""
    from sports_signal_bot.probabilistic.basketball.config import load_basketball_config
    from sports_signal_bot.probabilistic.basketball.expected_points import ExpectedPointsBuilder

    config = load_basketball_config()
    builder = ExpectedPointsBuilder()

    features = {
        "base_total_points": 218.0,
        "home_advantage_points": 3.5,
        "pace_adjustment": 5.0,
        "home_off_vs_away_def": 2.0,
        "away_off_vs_home_def": -1.0,
        "rating_diff": 4.0
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
def preview_basketball_market(event_id: str = "mock-basketball-1", market: str = "moneyline"):
    """Preview specific basketball markets derived from the model."""
    from sports_signal_bot.probabilistic.basketball.config import load_basketball_config
    from sports_signal_bot.probabilistic.basketball.registry import BASKETBALL_MODEL_REGISTRY

    config = load_basketball_config()
    model = BASKETBALL_MODEL_REGISTRY.get_model("basketball_normal_baseline", config)

    features = {
        "base_total_points": 220.5,
        "home_advantage_points": 3.0,
        "rating_diff": 6.0 # Home favored
    }

    records = model.predict(event_id, features)

    # Find the requested market
    record = next((r for r in records if r.market_type == market), None)

    if not record:
        console.print(f"[bold red]Market '{market}' not found in predictions.[/bold red]")
        console.print(f"Available markets: {[r.market_type for r in records]}")
        return

    console.print(f"[bold cyan]Market Preview: {market} for {event_id}[/bold cyan]")
    metrics = record.supporting_metrics
    console.print(f"Expected Total: {metrics['expected_total_points']:.2f} | Margin: {metrics['expected_margin_home']:.2f}")
    for k, v in record.predicted_probabilities.items():
        console.print(f"{k}: {v:.4f} ({v*100:.1f}%)")

@app.command()
def preview_basketball_diagnostics(event_id: str = "mock-basketball-1"):
    """Preview diagnostics for a basketball model run."""
    from sports_signal_bot.probabilistic.basketball.config import load_basketball_config
    from sports_signal_bot.probabilistic.basketball.expected_points import ExpectedPointsBuilder
    from sports_signal_bot.probabilistic.basketball.distribution import BasketballDistributionCore
    from sports_signal_bot.probabilistic.basketball.diagnostics import DiagnosticsBuilder

    config = load_basketball_config()
    builder = ExpectedPointsBuilder()
    dist_core = BasketballDistributionCore(config)

    features = {
        "base_total_points": 210.0,
        "total_std_modifier": 1.5 # artificially high variance
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
        features=features
    )

    console.print(f"[bold cyan]Diagnostics Preview for {event_id}[/bold cyan]")
    console.print(f"Implied Total: {diagnostics.implied_total:.2f}")
    console.print(f"Implied Margin: {diagnostics.implied_margin:.2f}")
    console.print(f"Total Variance: {diagnostics.total_variance:.2f} (STD: {total_std:.2f})")
    console.print(f"Margin Variance: {diagnostics.margin_variance:.2f} (STD: {margin_std:.2f})")

    if diagnostics.uncertainty_flags:
        console.print("[red]Uncertainty Flags:[/red]")
        for f in diagnostics.uncertainty_flags:
            console.print(f"  - {f}")

    if diagnostics.clipping_warnings:
        console.print("[yellow]Clipping Warnings:[/yellow]")
@app.command()
def build_training_dataset(sport: str, market: str):
    """Build a training dataset for the given sport and market type."""
    from sports_signal_bot.training.dataset import TrainingDatasetBuilder
    from sports_signal_bot.training.contracts import DatasetBuildConfig
    import pandas as pd
    from sports_signal_bot.core.paths import get_data_dir

    # In a real run, you'd load features and labels from the data tier
    # For now, let's mock it just to show it works
    console.print(f"[bold cyan]Building dataset for {sport} - {market}[/bold cyan]")

    # Mock data
    features_df = pd.DataFrame({
        'event_id': ['e1', 'e2', 'e3'],
        'event_datetime_utc': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'], utc=True),
        'feat1': [1.0, 2.0, 3.0],
        'feat2': [0.5, 0.5, 0.5]
    })
    labels_df = pd.DataFrame({
        'event_id': ['e1', 'e2', 'e3'],
        'market_type': [market, market, market],
        'label_name': [f'{sport}_{market}', f'{sport}_{market}', f'{sport}_{market}'],
        'class_index': [0, 1, 0],
        'validity_status': ['valid', 'valid', 'valid']
    })

    config = DatasetBuildConfig(sport=sport, market_type=market, label_name=f'{sport}_{market}')
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
    from sports_signal_bot.training.runner import TrainingRunManager
    import pandas as pd

    console.print(f"[bold cyan]Running training for {sport} - {market} using {model}[/bold cyan]")

    # Mock data
    features_df = pd.DataFrame({
        'event_id': ['e1', 'e2', 'e3', 'e4', 'e5'],
        'event_datetime_utc': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'], utc=True),
        'feat1': [1.0, 2.0, 3.0, 4.0, 5.0],
        'feat2': [0.5, 0.5, 0.5, 0.5, 0.5]
    })
    labels_df = pd.DataFrame({
        'event_id': ['e1', 'e2', 'e3', 'e4', 'e5'],
        'market_type': [market]*5,
        'label_name': [f'{sport}_{market}']*5,
        'class_index': [0, 1, 0, 1, 1],
        'validity_status': ['valid']*5
    })

    config = {
        'sport': sport,
        'market_type': market,
        'label_name': f'{sport}_{market}',
        'model_name': model,
        'split_strategy': 'holdout',
        'split_kwargs': {'train_fraction': 0.6, 'test_fraction': 0.0}
    }

    manager = TrainingRunManager(config)
    result = manager.run(features_df, labels_df)

    if result.get("status") == "success":
        console.print("[green]Training completed successfully![/green]")
        console.print(f"Run ID: {result['run_id']}")
        console.print(f"Output Dir: {result['output_dir']}")
        manifest = result['manifest']
        console.print(f"Metrics: {manifest.metrics_summary}")
    else:
        console.print(f"[bold red]Training failed:[/bold red] {result}")


@app.command()
def preview_splits(sport: str, market: str):
    """Preview how data would be split for training."""
    from sports_signal_bot.training.splits import HoldoutTimeSplit
    import pandas as pd

    console.print(f"[bold cyan]Previewing splits for {sport} - {market}[/bold cyan]")

    # Mock data
    df = pd.DataFrame({
        'event_id': [f'e{i}' for i in range(1, 11)],
        'event_datetime_utc': pd.date_range(start='2024-01-01', periods=10, freq='D')
    })

    splitter = HoldoutTimeSplit(train_fraction=0.7)
    for fold_id, train_idx, valid_idx, _ in splitter.split(df):
        console.print(f"Fold: {fold_id}")
        console.print(f"  Train: {len(train_idx)} rows (from {df.iloc[train_idx]['event_datetime_utc'].min().date()} to {df.iloc[train_idx]['event_datetime_utc'].max().date()})")
        console.print(f"  Valid: {len(valid_idx)} rows (from {df.iloc[valid_idx]['event_datetime_utc'].min().date()} to {df.iloc[valid_idx]['event_datetime_utc'].max().date()})")


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
    console.print(f"[bold cyan]Building calibration dataset for {sport} - {market}[/bold cyan]")
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
    from sports_signal_bot.calibration.runner import CalibrationRunner
    from sports_signal_bot.training.contracts import ValidationPredictionRecord
    from datetime import datetime, timezone

    console.print(f"[bold cyan]Running calibration for {sport} - {market} using {method}[/bold cyan]")

    # Mock data
    if "binary" in method:
        class_labels = ["0", "1"]
        predictions = [
            ValidationPredictionRecord(event_id="e1", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=1, predicted_class=1, predicted_probabilities={"0": 0.3, "1": 0.7}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
            ValidationPredictionRecord(event_id="e2", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=0, predicted_class=1, predicted_probabilities={"0": 0.4, "1": 0.6}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
            ValidationPredictionRecord(event_id="e3", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=1, predicted_class=1, predicted_probabilities={"0": 0.1, "1": 0.9}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
            ValidationPredictionRecord(event_id="e4", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=0, predicted_class=0, predicted_probabilities={"0": 0.8, "1": 0.2}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
        ]
    else:
        class_labels = ["A", "B", "C"]
        predictions = [
            ValidationPredictionRecord(event_id="e1", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=0, predicted_class=0, predicted_probabilities={"A": 0.7, "B": 0.2, "C": 0.1}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
            ValidationPredictionRecord(event_id="e2", sport=sport, market_type=market, label_name=f"{sport}_{market}", true_class_index=1, predicted_class=1, predicted_probabilities={"A": 0.3, "B": 0.5, "C": 0.2}, model_name="mock_model", fold_id="fold1", timestamp_utc=datetime.now(timezone.utc).isoformat()),
        ]

    config = {
        "sport": sport,
        "market_type": market,
        "label_name": f"{sport}_{market}",
        "method": method,
        "class_labels": class_labels,
        "source_model_run_id": "mock_run"
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
        console.print(f"[bold red]Calibration failed:[/bold red] {result.get('reason')}")

@app.command()
def preview_reliability(sport: str, market: str):
    """Preview reliability bins for a given market (stub)."""
    console.print(f"[bold cyan]Previewing reliability for {sport} - {market}[/bold cyan]")
    console.print("Bin 0: [0.0 - 0.1] Count: 100, Mean Pred: 0.05, Emp Freq: 0.04, Gap: 0.01")
    console.print("Bin 1: [0.1 - 0.2] Count: 150, Mean Pred: 0.15, Emp Freq: 0.16, Gap: -0.01")


if __name__ == '__main__':
    app()
