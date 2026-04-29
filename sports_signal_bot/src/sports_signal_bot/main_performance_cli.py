import typer
from .performance.runner import PerformanceRunner

app = typer.Typer(help="Performance and Runtime Optimization CLI")

@app.command()
def run_performance_pass(mode: str = "safe_default", sport: str = "all", market: str = "all"):
    typer.echo(f"Selected performance mode: {mode}")
    runner = PerformanceRunner(mode=mode)
    manifest = runner.run_pass(sport, market)
    typer.echo(f"Step timing summary generated.")
    typer.echo(f"Cache hit/miss summary generated.")
    typer.echo(f"Incremental/full recompute decision summary generated.")
    typer.echo(f"Bottleneck highlights generated.")
    typer.echo(f"Artifact path: results/performance/performance_manifest_{manifest.run_id}.json")

@app.command()
def preview_cache_health():
    typer.echo("Previewing cache health...")
    runner = PerformanceRunner()
    health = runner.preview_cache_health()
    typer.echo(health.model_dump_json(indent=2))

@app.command()
def preview_bottlenecks():
    typer.echo("Previewing bottlenecks...")
    runner = PerformanceRunner()
    bottlenecks = runner.preview_bottlenecks()
    typer.echo("No significant bottlenecks found." if not bottlenecks else "Bottlenecks listed in summary.")

@app.command()
def invalidate_cache(family: str = typer.Option(..., help="Cache family to invalidate")):
    runner = PerformanceRunner()
    res = runner.invalidate_cache(family)
    typer.echo(f"Invalidated cache family: {family}")

@app.command()
def cleanup_cache(mode: str = "maintenance"):
    runner = PerformanceRunner()
    res = runner.cleanup_cache(mode)
    typer.echo(f"Cache cleanup completed in mode: {mode}")

@app.command()
def preview_incremental_plan(sport: str = "all", market: str = "all"):
    runner = PerformanceRunner()
    plan = runner.preview_incremental_plan(sport, market)
    typer.echo("Incremental Plan:")
    typer.echo(plan.model_dump_json(indent=2))

@app.command()
def list_performance_modes():
    modes = [
        "safe_default",
        "inference_optimized",
        "backfill_optimized",
        "diagnostics_heavy",
        "maintenance_cleanup"
    ]
    typer.echo("Available Performance Modes:")
    for m in modes:
        typer.echo(f"- {m}")
