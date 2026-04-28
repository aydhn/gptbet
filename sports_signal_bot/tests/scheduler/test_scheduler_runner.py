from sports_signal_bot.scheduler.runner import SchedulerRunner
from sports_signal_bot.scheduler.contracts import ScheduledJobDefinition, SchedulerRunContext, SlotScheduleRecord, SlotType, SchedulerMode, JobState
import datetime

def test_scheduler_runner_strict_sequential():
    runner = SchedulerRunner("strict_sequential")
    jobs = [
        ScheduledJobDefinition(job_name="A", job_family="fam", job_runner_entrypoint="A", output_contract_name="outA"),
        ScheduledJobDefinition(job_name="B", job_family="fam", dependency_names=["A"], job_runner_entrypoint="B", output_contract_name="outB")
    ]
    context = SchedulerRunContext(
        schedule_run_id="run1",
        slot=SlotScheduleRecord(slot_id="slot1", slot_type=SlotType.morning, date=datetime.date.today(), start_time=datetime.time(10), end_time=datetime.time(11)),
        mode=SchedulerMode.execute
    )
    manifest = runner.run(jobs, context)
    assert manifest.summary.planned_jobs == 2
    assert manifest.summary.executed_jobs == 2
    assert len(manifest.executions) == 2
    assert manifest.executions[0].job_name == "A"
    assert manifest.executions[0].state_after == JobState.succeeded
    assert manifest.executions[1].job_name == "B"
    assert manifest.executions[1].state_after == JobState.succeeded

def test_scheduler_runner_dry_run():
    runner = SchedulerRunner("strict_sequential")
    jobs = [
        ScheduledJobDefinition(job_name="A", job_family="fam", job_runner_entrypoint="A", output_contract_name="outA")
    ]
    context = SchedulerRunContext(
        schedule_run_id="run2",
        slot=SlotScheduleRecord(slot_id="slot2", slot_type=SlotType.morning, date=datetime.date.today(), start_time=datetime.time(10), end_time=datetime.time(11)),
        mode=SchedulerMode.dry_run
    )
    manifest = runner.run(jobs, context)
    assert manifest.executions[0].state_after == JobState.dry_run_only
