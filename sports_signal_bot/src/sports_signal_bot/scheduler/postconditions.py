from typing import Dict, Any, List
from .contracts import JobPostconditionRecord, ScheduledJobDefinition

def evaluate_job_postconditions(job: ScheduledJobDefinition, execution_context: Dict[str, Any]) -> List[JobPostconditionRecord]:
    records = []

    manifest_path = execution_context.get("manifest_path")
    if job.postconditions and "manifest_exists" in job.postconditions:
        if not manifest_path:
            records.append(JobPostconditionRecord(
                check_name="manifest_exists",
                passed=False,
                reason="Expected manifest was not generated"
            ))
        else:
            records.append(JobPostconditionRecord(
                check_name="manifest_exists",
                passed=True,
                reason="Manifest generated"
            ))

    return records

def summarize_postcondition_failures(records: List[JobPostconditionRecord]) -> str:
    failures = [r.reason for r in records if not r.passed]
    return " | ".join(failures)
