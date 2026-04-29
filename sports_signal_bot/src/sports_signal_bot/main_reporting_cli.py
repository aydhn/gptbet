import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from sports_signal_bot.reporting.runner import ReportingRunner
from sports_signal_bot.reporting.reporting import ReportingReporter
from sports_signal_bot.reporting.contracts import ReportingManifest
from sports_signal_bot.reporting.registry import MetricRegistry
from datetime import datetime
import uuid

app = typer.Typer(help="Reporting, Metrics, and KPI Governance Commands")
console = Console()

@app.command()
def run_reporting(
    audience: str = typer.Option("executive", "--audience", "-a", help="Audience profile (executive, operator, maintainer)"),
    period: str = typer.Option("daily", "--period", "-p", help="Reporting period (slot, daily, weekly)"),
    output_dir: str = typer.Option("artifacts/reporting", "--output-dir", "-o", help="Directory to save report artifacts")
):
    """Run period consolidation and generate audience-aware report bundles."""
    console.print(f"Running reporting for audience [bold blue]{audience}[/bold blue], period [bold green]{period}[/bold green]...")

    config_dir = Path("configs/reporting")
    runner = ReportingRunner(config_dir)

    try:
        bundle = runner.run(audience, period)
    except Exception as e:
        console.print(f"[bold red]Error running report:[/bold red] {e}")
        raise typer.Exit(code=1)

    out_path = Path(output_dir)
    reporter = ReportingReporter(out_path)

    j_path = reporter.write_json_bundle(bundle)
    m_path = reporter.write_markdown_summary(bundle)
    c_path = reporter.write_csv_extracts(bundle)

    manifest = ReportingManifest(
        manifest_id=f"rep_{uuid.uuid4().hex[:8]}",
        created_at=datetime.now(),
        bundle=bundle
    )
    r_path = reporter.write_manifest(manifest)

    console.print("\n[bold]Report Summary[/bold]")
    console.print(f"Sections generated: {len(bundle.sections)}")
    console.print(f"KPIs evaluated: {len(bundle.kpi_bundle.kpis)}")
    console.print(f"Warnings/Caveats: {len(bundle.warnings_caveats)}")

    console.print("\n[bold]Artifacts written:[/bold]")
    console.print(f"- {j_path}")
    console.print(f"- {m_path}")
    console.print(f"- {c_path}")
    console.print(f"- {r_path}")

@app.command()
def list_kpis():
    """List all registered KPIs and their target directionality."""
    config_dir = Path("configs/reporting")
    registry = MetricRegistry(config_dir)
    kpis = registry.list_kpis()

    table = Table(title="Registered KPIs")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Family", style="green")
    table.add_column("Direction", style="yellow")

    for k in kpis:
        table.add_row(k.kpi_id, k.name, k.family, k.directionality)

    console.print(table)

@app.command()
def preview_report_bundle(
    audience: str = typer.Option("operator", "--audience", "-a"),
    period: str = typer.Option("daily", "--period", "-p")
):
    """Preview a report bundle generation without writing to disk."""
    console.print(f"Previewing bundle for [bold]{audience}[/bold] / [bold]{period}[/bold]...")
    config_dir = Path("configs/reporting")
    runner = ReportingRunner(config_dir)

    bundle = runner.run(audience, period)
    console.print(bundle.model_dump_json(indent=2))
