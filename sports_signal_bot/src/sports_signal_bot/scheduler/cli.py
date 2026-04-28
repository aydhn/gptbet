import typer
import datetime
from .contracts import SlotType, SchedulerMode, SchedulerRunContext, SlotScheduleRecord, ScheduledJobDefinition
from .runner import SchedulerRunner
from .manifests import SchedulerManifestWriter
from typing import List

app = typer.Typer(help="Scheduled Orchestration Commands")

def get_dummy_jobs() -> List[ScheduledJobDefinition]:
    return [
        ScheduledJobDefinition(job_name="ingest", job_family="ingest", job_runner_entrypoint="ingest", output_contract_name="ingest_manifest"),
        ScheduledJobDefinition(job_name="inference", job_family="inference", dependency_names=["ingest"], job_runner_entrypoint="inference", output_contract_name="inference_manifest"),
        ScheduledJobDefinition(job_name="dispatch", job_family="dispatch", dependency_names=["inference"], job_runner_entrypoint="dispatch", output_contract_name="dispatch_manifest"),
        ScheduledJobDefinition(job_name="monitoring", job_family="monitoring", dependency_names=["dispatch"], job_runner_entrypoint="monitoring", output_contract_name="monitoring_manifest")
    ]

@app.command(name="run-scheduler")
def run_scheduler(
    slot: SlotType = typer.Option(..., help="Slot to run"),
    strategy: str = typer.Option("strict_sequential", help="Scheduler strategy"),
    runbook: str = typer.Option(None, help="Runbook to use"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Run in dry_run mode")
):
    typer.echo(f"Starting scheduler run for slot: {slot.value}")

    context = SchedulerRunContext(
        schedule_run_id=f"run_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        slot=SlotScheduleRecord(
            slot_id=slot.value,
            slot_type=slot,
            date=datetime.date.today(),
            start_time=datetime.time(12, 0),
            end_time=datetime.time(13, 0)
        ),
        mode=SchedulerMode.dry_run if dry_run else SchedulerMode.execute
    )

    jobs = get_dummy_jobs()
    runner = SchedulerRunner(strategy_name=strategy)
    manifest = runner.run(jobs, context)

    writer = SchedulerManifestWriter("results/scheduler")
    writer.write(manifest)

    typer.echo(f"Run completed. Planned: {manifest.summary.planned_jobs}, Executed: {manifest.summary.executed_jobs}")
    typer.echo(f"Manifest written to results/scheduler/scheduler_manifest_{manifest.schedule_run_id}.json")

@app.command(name="preview-slot-plan")
def preview_slot_plan(slot: SlotType = typer.Option(..., help="Slot to preview")):
    context = SchedulerRunContext(
        schedule_run_id="preview",
        slot=SlotScheduleRecord(slot_id=slot.value, slot_type=slot, date=datetime.date.today(), start_time=datetime.time(12, 0), end_time=datetime.time(13, 0)),
        mode=SchedulerMode.planned_only
    )
    jobs = get_dummy_jobs()
    runner = SchedulerRunner("strict_sequential")
    plan = runner.strategy.plan(jobs, context)
    typer.echo(f"Previewing slot plan for {slot.value}:")
    typer.echo(f"Execution Order: {' -> '.join(plan)}")

@app.command(name="list-scheduled-jobs")
def list_scheduled_jobs():
    jobs = get_dummy_jobs()
    for job in jobs:
        typer.echo(f"- {job.job_name} ({job.job_family}) [deps: {job.dependency_names}]")
