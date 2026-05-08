import typer
import json
from rich.console import Console
from rich.table import Table

from sports_signal_bot.concurrency_hardening.integration import run_concurrency_hardening_pass
from sports_signal_bot.concurrency_hardening.utils import write_json_artifact

app = typer.Typer(help="Concurrency Hardening Pack 03 Commands")
console = Console()

@app.command("run-hardening-pack-03")
def run_hardening_pack_03(
    strategy: str = typer.Option("ConservativeConcurrencyHardeningStrategy", help="The concurrency hardening strategy to use."),
    output_dir: str = typer.Option(".", help="Directory to save artifacts.")
):
    """Runs the full post-100 hardening pack 03 for concurrency and async discipline."""
    console.print(f"[bold blue]Running Concurrency Hardening Pack 03 using {strategy}...[/bold blue]")

    results = run_concurrency_hardening_pass(strategy)

    # Write artifacts
    write_json_artifact(f"{output_dir}/concurrency_guards.json", results["manifests"]["guards"])
    write_json_artifact(f"{output_dir}/parallel_execution_plans.json", results["manifests"]["parallelism"])
    write_json_artifact(f"{output_dir}/async_ordering_report.json", results["manifests"]["ordering"])
    write_json_artifact(f"{output_dir}/race_probe_runs.json", results["manifests"]["race_probes"])
    write_json_artifact(f"{output_dir}/shared_state_report.json", results["manifests"]["shared_state"])
    write_json_artifact(f"{output_dir}/idempotency_report.json", results["manifests"]["idempotency"])
    write_json_artifact(f"{output_dir}/stale_read_report.json", results["manifests"]["stale_reads"])
    write_json_artifact(f"{output_dir}/queue_discipline_report.json", results["manifests"]["queues"])
    write_json_artifact(f"{output_dir}/timeout_cancellation_report.json", results["manifests"]["timeouts"])
    write_json_artifact(f"{output_dir}/concurrency_regressions.json", results["manifests"]["regressions"])
    write_json_artifact(f"{output_dir}/concurrency_hardening_health_report.json", results["overall_health"])

    # Print summary
    health = results["overall_health"]
    color = "green" if health["is_healthy"] else "red"
    console.print(f"[{color}]Health: {health['status_summary']}[/{color}]")
    console.print(f"Release Blockers: {health['blocker_count']}")
    console.print(f"Artifacts generated in {output_dir}/")

@app.command("preview-concurrency-guard-report")
def preview_concurrency_guard_report():
    """Previews the concurrency guard report."""
    results = run_concurrency_hardening_pass()
    guards = results["manifests"]["guards"]["guards"]

    table = Table(title="Concurrency Guards")
    table.add_column("Guard ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Status", style="green")

    for g in guards:
        status_color = "green" if g["guard_status"] == "guard_safe" else "yellow"
        table.add_row(g["concurrency_guard_id"], g["guard_family"], f"[{status_color}]{g['guard_status']}[/{status_color}]")

    console.print(table)

@app.command("preview-parallelism-report")
def preview_parallelism_report():
    """Previews the bounded parallelism report."""
    results = run_concurrency_hardening_pass()
    plans = results["manifests"]["parallelism"]["plans"]

    table = Table(title="Parallel Execution Plans")
    table.add_column("Plan ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Max Parallelism", justify="right")
    table.add_column("Status", style="green")

    for p in plans:
        status_color = "green" if p["plan_status"] == "plan_safe" else "red"
        table.add_row(p["parallel_plan_id"], p["plan_family"], str(p["max_parallelism"]), f"[{status_color}]{p['plan_status']}[/{status_color}]")

    console.print(table)

@app.command("list-concurrency-hardening-strategies")
def list_concurrency_hardening_strategies():
    """Lists available concurrency hardening strategies."""
    console.print("[bold]Available Strategies:[/bold]")
    console.print("- ConservativeConcurrencyHardeningStrategy (Default, strict safety)")
    console.print("- BalancedBoundedParallelismStrategy (Balanced throughput and safety)")
    console.print("- AsyncSafetyFirstStrategy (Prioritizes async ordering and cancellation)")


@app.command("preview-async-ordering-report")
def preview_async_ordering_report():
    """Previews the async ordering report."""
    results = run_concurrency_hardening_pass()
    orderings = results["manifests"]["ordering"]["orderings"]
    table = Table(title="Async Orderings")
    table.add_column("Ordering ID", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="green")
    for o in orderings:
        status_color = "green" if o["status"] == "ordering_safe" else "yellow"
        table.add_row(o["ordering_id"], o["target_ref"], f"[{status_color}]{o['status']}[/{status_color}]")
    console.print(table)

@app.command("preview-race-probe-report")
def preview_race_probe_report():
    """Previews the race probe report."""
    results = run_concurrency_hardening_pass()
    runs = results["manifests"]["race_probes"]["runs"]
    table = Table(title="Race Probe Runs")
    table.add_column("Run ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Violations Detected", justify="right")
    for r in runs:
        status_color = "green" if r["run_status"] == "race_clean" else "red"
        table.add_row(r["run_id"], f"[{status_color}]{r['run_status']}[/{status_color}]", str(r["violations_detected"]))
    console.print(table)

@app.command("preview-idempotency-report")
def preview_idempotency_report():
    """Previews the idempotency report."""
    results = run_concurrency_hardening_pass()
    records = results["manifests"]["idempotency"]["records"]
    table = Table(title="Idempotency Records")
    table.add_column("ID", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="green")
    for r in records:
        status_color = "green" if r["status"] == "protected" else "yellow"
        table.add_row(r["idempotency_id"], r["target_ref"], f"[{status_color}]{r['status']}[/{status_color}]")
    console.print(table)

@app.command("preview-queue-discipline-report")
def preview_queue_discipline_report():
    """Previews the queue discipline report."""
    results = run_concurrency_hardening_pass()
    disciplines = results["manifests"]["queues"]["disciplines"]
    table = Table(title="Queue Disciplines")
    table.add_column("ID", style="cyan")
    table.add_column("Target Queue", style="magenta")
    table.add_column("Status", style="green")
    for d in disciplines:
        status_color = "green" if d["status"] == "monitored" else "yellow"
        table.add_row(d["discipline_id"], d["target_queue"], f"[{status_color}]{d['status']}[/{status_color}]")
    console.print(table)

@app.command("preview-concurrency-hardening-health")
def preview_concurrency_hardening_health():
    """Previews the overall concurrency hardening health report."""
    results = run_concurrency_hardening_pass()
    health = results["overall_health"]
    color = "green" if health["is_healthy"] else "red"
    console.print(f"[{color}]Overall Health: {health['status_summary']}[/{color}]")
    console.print(f"Release Blockers: {health['blocker_count']}")

if __name__ == "__main__":
    app()
