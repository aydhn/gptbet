from typing import Dict, Any, List
from .contracts import JobPreconditionRecord, ScheduledJobDefinition

def evaluate_job_preconditions(job: ScheduledJobDefinition, system_state: Dict[str, Any]) -> List[JobPreconditionRecord]:
    records = []

    # Example logic: checking freeze/degrade vs job settings
    freeze_active = system_state.get("freeze_active", False)
    if freeze_active and job.freeze_behavior == "block":
        records.append(JobPreconditionRecord(
            check_name="freeze_check",
            passed=False,
            reason="System freeze is active and job block policy is active"
        ))
    else:
        records.append(JobPreconditionRecord(check_name="freeze_check", passed=True, reason="Freeze check passed"))

    degrade_active = system_state.get("degrade_active", False)
    if degrade_active and job.degrade_behavior == "block":
         records.append(JobPreconditionRecord(
            check_name="degrade_check",
            passed=False,
            reason="System degrade is active and job block policy is active"
        ))
    else:
        records.append(JobPreconditionRecord(check_name="degrade_check", passed=True, reason="Degrade check passed"))

    return records

def summarize_precondition_failures(records: List[JobPreconditionRecord]) -> str:
    failures = [r.reason for r in records if not r.passed]
    return " | ".join(failures)
