import pytest
from sports_signal_bot.scheduler.contracts import ScheduledJobDefinition
from sports_signal_bot.scheduler.preconditions import evaluate_job_preconditions

def test_evaluate_job_preconditions():
    job = ScheduledJobDefinition(job_name="A", job_family="fam", freeze_behavior="block", job_runner_entrypoint="A", output_contract_name="out")

    # Normal state
    records = evaluate_job_preconditions(job, system_state={"freeze_active": False})
    for r in records:
        assert r.passed == True

    # Freeze active
    records = evaluate_job_preconditions(job, system_state={"freeze_active": True})
    freeze_check = [r for r in records if r.check_name == "freeze_check"][0]
    assert freeze_check.passed == False
