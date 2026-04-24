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
