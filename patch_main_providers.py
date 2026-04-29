import re

with open("sports_signal_bot/src/sports_signal_bot/main.py", "r") as f:
    content = f.read()

# Add imports for providers
new_imports = """
from sports_signal_bot.providers.contracts import DataFamily
from sports_signal_bot.providers.requests import build_provider_request
from sports_signal_bot.providers.adapters.stub_test_provider import StubTestProviderAdapter
from sports_signal_bot.providers.registry import ProviderRegistry
from sports_signal_bot.providers.quality import ProviderQualityScorer
from sports_signal_bot.providers.health import build_provider_health_snapshot, classify_provider_health
from sports_signal_bot.providers.failover import ProviderFailoverEngine
"""

content = content.replace("import typer\n", "import typer\n" + new_imports)

new_commands = """

@app.command()
def fetch_provider_data(sport: str = typer.Option(...), family: str = typer.Option(...), mode: str = typer.Option("ops"), dry_run: bool = typer.Option(False)):
    \"\"\"Fetch data from a provider via the abstraction layer.\"\"\"
    console.print(f"[bold green]Fetching provider data for sport: {sport}, family: {family}, mode: {mode}[/bold green]")
    registry = ProviderRegistry()
    registry.register("stub_test_provider", StubTestProviderAdapter("stub_test_provider"))

    data_family_enum = DataFamily(family)
    request = build_provider_request(sport=sport, data_family=data_family_enum, mode=mode)

    adapter = registry.get("stub_test_provider")
    if adapter:
        if dry_run:
            res = adapter.dry_run_preview(request)
            console.print("[yellow]DRY RUN PREVIEW[/yellow]")
        else:
            res = adapter.fetch(request)
        console.print(f"Provider Used: {res.provider_used}")
        console.print(f"Records Fetched: {len(res.records)}")
        if res.quality_summary:
            console.print(f"Quality Score: {res.quality_summary.overall_score}")
    else:
        console.print("[red]Provider not found[/red]")

@app.command()
def preview_provider_health():
    \"\"\"Preview health of configured providers.\"\"\"
    console.print("[bold blue]Previewing Provider Health[/bold blue]")
    health = build_provider_health_snapshot("stub_test_provider")
    status = classify_provider_health(health)
    console.print(f"Provider: {health.provider_name} - Status: {status.value}")

@app.command()
def preview_provider_quality(family: str = typer.Option(...)):
    \"\"\"Preview quality scores for a given data family.\"\"\"
    console.print(f"[bold blue]Previewing Provider Quality for {family}[/bold blue]")
    scorer = ProviderQualityScorer()
    # Dummy fetch time and payload
    from datetime import datetime
    res = scorer.score_payload({"dummy": "data"}, family, datetime.utcnow())
    console.print(scorer.explain_provider_quality(res))

@app.command()
def preview_provider_failovers():
    \"\"\"Preview configured provider failover sequences.\"\"\"
    console.print("[bold blue]Previewing Provider Failovers[/bold blue]")
    engine = ProviderFailoverEngine({"failover_sequences": {"stub_test_provider": ["local_file_feed", "manual_import_provider"]}})
    console.print(f"stub_test_provider failovers: {engine.get_next_provider('stub_test_provider', 0)}, {engine.get_next_provider('stub_test_provider', 1)}")

@app.command()
def list_providers():
    \"\"\"List all registered providers in the abstraction layer.\"\"\"
    console.print("[bold green]Registered Providers:[/bold green]")
    registry = ProviderRegistry()
    registry.register("stub_test_provider", StubTestProviderAdapter("stub_test_provider"))
    for p in registry.list_all():
        console.print(f"- {p}")
"""

content = content + new_commands

with open("sports_signal_bot/src/sports_signal_bot/main.py", "w") as f:
    f.write(content)
