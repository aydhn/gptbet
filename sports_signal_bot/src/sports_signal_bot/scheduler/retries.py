from typing import Dict, Any
from .contracts import RetryDecisionRecord

def classify_job_failure(error_type: str, job_family: str) -> str:
    if "ConnectionError" in error_type: return "transient"
    if "Timeout" in error_type: return "transient"
    if "ValidationError" in error_type: return "fatal"
    return "unknown"

def compute_retry_delay(attempt: int, policy: str) -> int:
    if policy == "immediate_retry_once" and attempt == 1: return 0
    if policy == "bounded_retry_with_backoff": return min(300, 30 * (2 ** (attempt - 1)))
    return 0

def decide_retry_action(job_name: str, attempt: int, policy: str, error_type: str, job_family: str) -> RetryDecisionRecord:
    failure_category = classify_job_failure(error_type, job_family)

    if policy == "no_retry":
        return RetryDecisionRecord(job_name=job_name, attempt_number=attempt, will_retry=False, delay_seconds=0, reason="Policy restricts retries")

    if failure_category == "fatal":
        return RetryDecisionRecord(job_name=job_name, attempt_number=attempt, will_retry=False, delay_seconds=0, reason="Fatal error type")

    if policy == "immediate_retry_once" and attempt <= 1:
        return RetryDecisionRecord(job_name=job_name, attempt_number=attempt, will_retry=True, delay_seconds=0, reason="Immediate retry permitted")

    if policy == "bounded_retry_with_backoff" and attempt <= 3:
        delay = compute_retry_delay(attempt, policy)
        return RetryDecisionRecord(job_name=job_name, attempt_number=attempt, will_retry=True, delay_seconds=delay, reason="Backoff retry permitted")

    return RetryDecisionRecord(job_name=job_name, attempt_number=attempt, will_retry=False, delay_seconds=0, reason="Max attempts reached")

def stop_retry_storm(recent_failures: int, threshold: int = 10) -> bool:
    return recent_failures >= threshold
