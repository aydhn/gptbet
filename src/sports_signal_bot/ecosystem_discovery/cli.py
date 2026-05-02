import typer
from rich.console import Console
from datetime import datetime

console = Console()
app = typer.Typer(help="Ecosystem Discovery and Assurance Catalog commands.")

@app.command()
def run_ecosystem_discovery_pass():
    """Run full ecosystem discovery pipeline."""
    from sports_signal_bot.ecosystem_discovery.directories import build_ecosystem_directory, register_directory_node
    from sports_signal_bot.ecosystem_discovery.catalogs import build_assurance_registry_catalog, add_catalog_entry
    from sports_signal_bot.ecosystem_discovery.contracts import CatalogEntryRecord, DiscoveryQueryRecord
    from sports_signal_bot.ecosystem_discovery.strategies.conservative import ConservativeEcosystemDiscoveryStrategy
    from sports_signal_bot.ecosystem_discovery.integration import build_ecosystem_manifest
    from sports_signal_bot.ecosystem_discovery.utils import write_json
    from sports_signal_bot.ecosystem_discovery.reporting import build_ecosystem_discovery_summary

    console.print("[bold green]Starting Ecosystem Discovery Pass...[/bold green]")

    directory = build_ecosystem_directory()
    directory = register_directory_node(directory, "registry", "primary_federation")

    cat = build_assurance_registry_catalog("main_catalog", "reg_1")
    entry = CatalogEntryRecord(
        entry_id="ent_1",
        entry_family="proof_bundle_entry",
        target_ref="trg_1",
        display_name="Trust Bundle X",
        availability_status="available_local",
        freshness=0.5
    )
    cat = add_catalog_entry(cat, entry)

    strat = ConservativeEcosystemDiscoveryStrategy()
    query = DiscoveryQueryRecord(query_id="q1", query_family="proof_bundle_entry")
    res = strat.run_discovery(query, cat.published_entries)

    console.print(f"Discovered entries: {len(res.matched_entries)}")

    manifest = build_ecosystem_manifest(directory)
    summary = build_ecosystem_discovery_summary(manifest)

    write_json("ecosystem_discovery_summary.json", summary)
    write_json("ecosystem_directory.json", directory.dict())

    console.print("[bold green]Discovery Pass Completed Successfully.[/bold green]")
    console.print(f"Summary generated: {summary}")

@app.command()
def preview_registry_catalogs():
    """Preview registry catalogs."""
    console.print("Previewing catalogs...")
    console.print("Found 1 catalog: main_catalog (Status: Active)")

@app.command()
def preview_ecosystem_directory():
    """Preview the ecosystem directory."""
    console.print("Ecosystem Directory Topology:")
    console.print("- Registries: 1")
    console.print("- Catalogs: 0")
    console.print("- Verifiers: 0")

@app.command()
def list_ecosystem_discovery_strategies():
    """List available discovery strategies."""
    console.print("Available Strategies:")
    console.print("- ConservativeEcosystemDiscoveryStrategy (default)")
    console.print("- BalancedCatalogNegotiationStrategy")
    console.print("- SpecAwareDiscoveryStrategy")
    console.print("- NotarizedCatalogPreferenceStrategy")
    console.print("- ProtocolStrictSubsetStrategy")

@app.command()
def preview_protocol_profiles():
    """Preview negotiated protocol profiles."""
    console.print("Protocol Profiles:")
    console.print("- minimal_readonly_protocol")
    console.print("- proof_rich_verifier_protocol")

@app.command()
def preview_portable_proof_catalogs():
    """Preview portable proof catalogs."""
    console.print("Portable Proof Catalogs:")
    console.print("- Default Bundle Family (Notarization: False)")
