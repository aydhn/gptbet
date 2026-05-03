import typer
from rich.console import Console
from rich.table import Table
import json

app = typer.Typer(help="Execution coordination fabric operations (Phase 73)")
console = Console()

@app.command()
def run_execution_coordination_pass():
    """Run a single pass of the execution coordination fabric"""
    from src.sports_signal_bot.execution_coordination.fabric import SupervisedExecutionCoordinationFabric
    from src.sports_signal_bot.execution_coordination.contracts import PriorityBand, SchedulingWindowRecord
    import datetime

    fabric = SupervisedExecutionCoordinationFabric()
    window = SchedulingWindowRecord(
        window_id="win_1",
        start_time=datetime.datetime.now(datetime.timezone.utc),
        end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        max_parallel_lanes=2
    )

    console.print("Admitting lanes into scheduler...")
    fabric.admit_lane("lane_recovery_A", PriorityBand.CRITICAL_RECOVERY, window)
    fabric.admit_lane("lane_recovery_B", PriorityBand.CRITICAL_RECOVERY, window)

    console.print("Running coordination pass (broker, contention, arbitration, scheduler)...")
    fabric.coordinate()

    summary = fabric.get_summary()

    console.print(f"[green]Coordination pass complete. Fabric Status: {summary.coordination_status}[/green]")
    console.print(f"Active Lanes: {len(summary.active_lane_refs)}")
    console.print(f"Waiting Lanes: {len(summary.queue_refs)}")
    console.print(f"Contentions Resolved: {len(summary.arbitration_refs)}")

@app.command()
def preview_multi_lane_schedules():
    """Preview current multi-lane schedules"""
    console.print("Previewing schedules...")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Lane Ref")
    table.add_column("Priority")
    table.add_column("Status")
    table.add_row("lane_recovery_A", "CRITICAL_RECOVERY", "SCHEDULE_RUNTIME_ASSIGNED")
    table.add_row("lane_recovery_B", "CRITICAL_RECOVERY", "SCHEDULE_WAITING_ARBITRATION")
    console.print(table)

@app.command()
def list_execution_coordination_strategies():
    """List available coordination strategies"""
    from src.sports_signal_bot.execution_coordination.strategies import (
        ConservativeCoordinationFabricStrategy,
        BalancedMultiLaneFabricStrategy,
        RollbackClosurePriorityStrategy
    )

    console.print("Available execution coordination strategies:")
    strategies = [
        ConservativeCoordinationFabricStrategy().name(),
        BalancedMultiLaneFabricStrategy().name(),
        RollbackClosurePriorityStrategy().name()
    ]

    for s in strategies:
        console.print(f"- {s}")

if __name__ == "__main__":
    app()
