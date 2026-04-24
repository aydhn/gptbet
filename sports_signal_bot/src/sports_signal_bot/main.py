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

if __name__ == "__main__":
    app()

from sports_signal_bot.markets.registry import MARKET_REGISTRY
from sports_signal_bot.labels.generator import LabelGenerator
from sports_signal_bot.results.contracts import EventResultRecord
from sports_signal_bot.audit.leakage import detect_post_event_snapshot_leakage
from sports_signal_bot.benchmark.factory import BENCHMARK_FACTORY
from sports_signal_bot.data.contracts.canonical import CanonicalOddsRecord
from sports_signal_bot.core.constants import SportType
from datetime import datetime
import pandas as pd
from pydantic import ValidationError

@app.command()
def generate_labels(sport: str = typer.Option(..., help="Sport to generate labels for")):
    """Generate labels from sample result data."""
    try:
        sport_enum = SportType(sport)
    except ValueError:
        console.print(f"[red]Invalid sport: {sport}[/red]")
        return

    markets = MARKET_REGISTRY.list_supported_markets(sport_enum)
    line_sets = {m.market_type: MARKET_REGISTRY.get_default_lines(m.market_type) for m in markets}

    generator = LabelGenerator(markets, line_sets)

    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"
    if not results_path.exists():
        console.print(f"[red]Results sample not found: {results_path}[/red]")
        return

    df = pd.read_csv(results_path)
    # Replace nan with None
    df = df.where(pd.notnull(df), None)

    console.print(f"[bold green]Generating Labels for {sport}[/bold green]")
    for _, row in df.iterrows():
        try:
            # handle timestamp
            ts_val = row.get('result_timestamp_utc')
            ts = None
            if ts_val is not None:
                ts = datetime.fromisoformat(ts_val.replace("Z", "+00:00"))

            rec = EventResultRecord(
                event_id=row['event_id'],
                sport=sport_enum,
                status=row['status'],
                final_home_score=row.get('final_home_score'),
                final_away_score=row.get('final_away_score'),
                result_timestamp_utc=ts,
                result_source=row['result_source']
            )
            labels = generator.generate(rec)
            console.print(f"\n[cyan]Event: {rec.event_id} ({rec.status})[/cyan]")
            for label in labels:
                color = "green" if label.validity_status.value == "valid" else "yellow"
                console.print(f"  [{color}]{label.label_name}: {label.target_text} ({label.validity_status.value})[/{color}]")
        except ValidationError as e:
            console.print(f"[red]Validation error on row {row['event_id']}: {e}[/red]")

@app.command()
def list_markets(sport: str = typer.Option(..., help="Sport to list markets for")):
    """List canonical markets registered for the sport."""
    try:
        sport_enum = SportType(sport)
    except ValueError:
        console.print(f"[red]Invalid sport: {sport}[/red]")
        return

    markets = MARKET_REGISTRY.list_supported_markets(sport_enum)
    console.print(f"[bold blue]Registered Markets for {sport}:[/bold blue]")
    for m in markets:
        lines = MARKET_REGISTRY.get_default_lines(m.market_type)
        line_str = f", Lines: {lines}" if lines else ""
        console.print(f"  - {m.market_type} (Rule: {m.settlement_rule_name}{line_str})")

@app.command()
def run_benchmark_preview(sport: str = typer.Option(...), market: str = typer.Option(...)):
    """Preview benchmark outputs using sample odds."""
    try:
        sport_enum = SportType(sport)
    except ValueError:
        console.print(f"[red]Invalid sport: {sport}[/red]")
        return

    market_def = MARKET_REGISTRY.get_market_definition(sport_enum, market)
    if not market_def:
        console.print(f"[red]Market {market} not found for {sport}[/red]")
        return

    odds_path = get_data_dir() / "sample_inputs" / sport / "odds_sample.csv"
    if not odds_path.exists():
        console.print(f"[red]Odds sample not found: {odds_path}[/red]")
        return

    df = pd.read_csv(odds_path)
    df = df.where(pd.notnull(df), None)

    # We will use the bookmaker_implied benchmark
    benchmark = BENCHMARK_FACTORY.get_benchmark("bookmaker_implied")

    console.print(f"[bold green]Running Benchmark Preview for {market}[/bold green]")
    # Group by event
    for event_id, group in df.groupby('event_id'):
        snapshots = []
        for _, row in group.iterrows():
            # For preview, we match simplified market types mapping if needed
            # In real system, proper mapping layer handles this
            m_type_raw = str(row['market_type']).upper().replace("1X2", "FOOTBALL_1X2")
            if "FOOTBALL" not in m_type_raw and sport_enum == SportType.FOOTBALL:
                m_type_raw = f"FOOTBALL_{m_type_raw}"
            if "BASKETBALL" not in m_type_raw and sport_enum == SportType.BASKETBALL:
                 m_type_raw = f"BASKETBALL_{m_type_raw}"

            # Match strictly with expected market
            if m_type_raw.lower() != market.lower():
                continue

            snapshots.append(CanonicalOddsRecord(
                event_id=row['event_id'],
                market_type=m_type_raw, # Assuming enum match for now
                bookmaker=row['bookmaker'],
                snapshot_ts_utc=datetime.fromisoformat(row['snapshot_ts_utc'].replace("Z", "+00:00")),
                selection=row['selection'],
                decimal_odds=row['decimal_odds'],
                implied_probability=1.0/row['decimal_odds'] if row['decimal_odds'] > 0 else 0,
                handicap_line=row.get('handicap_line'),
                total_line=row.get('total_line')
            ))

        if snapshots:
             pred = benchmark.generate_prediction(event_id, market_def, {"odds_snapshot": snapshots})
             console.print(f"Event: {event_id} -> {pred.predicted_class} {pred.predicted_probabilities}")
        else:
             console.print(f"Event: {event_id} -> No matching odds found")

@app.command()
def audit_leakage(sport: str = typer.Option(...)):
    """Run leakage audit on sample results and odds."""
    console.print(f"[bold blue]Auditing Leakage for {sport}[/bold blue]")
    # Simplified simulation using our sample files
    odds_path = get_data_dir() / "sample_inputs" / sport / "odds_sample.csv"
    results_path = get_data_dir() / "sample_inputs" / sport / "results_sample.csv"

    if not odds_path.exists() or not results_path.exists():
         console.print("[yellow]Sample files missing.[/yellow]")
         return

    odds_df = pd.read_csv(odds_path)
    res_df = pd.read_csv(results_path)

    # Let's say event start time is derived from result file or mock
    # For simulation, assume event start time is 2 hours before result_timestamp
    from datetime import timedelta

    for _, res_row in res_df.iterrows():
        if pd.isna(res_row['result_timestamp_utc']): continue

        event_id = res_row['event_id']
        res_ts = datetime.fromisoformat(res_row['result_timestamp_utc'].replace("Z", "+00:00"))
        event_start = res_ts - timedelta(hours=2)

        event_odds = odds_df[odds_df['event_id'] == event_id]
        for _, odd_row in event_odds.iterrows():
            snap_ts = datetime.fromisoformat(odd_row['snapshot_ts_utc'].replace("Z", "+00:00"))

            audit = detect_post_event_snapshot_leakage(event_start, snap_ts, event_id, odd_row['market_type'])
            if audit.audit_status == "fail":
                console.print(f"[bold red]LEAKAGE DETECTED[/bold red]: Event {event_id} - {audit.message}")
            else:
                 console.print(f"[green]PASS[/green]: Event {event_id} - Odds at {snap_ts} (Start: {event_start})")
