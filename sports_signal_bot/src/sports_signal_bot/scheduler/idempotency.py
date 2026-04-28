from typing import Dict, Any

def build_job_idempotency_key(job_name: str, slot_id: str, date_str: str) -> str:
    return f"{date_str}_{slot_id}_{job_name}"

def detect_duplicate_scheduled_run(idempotency_key: str, execution_ledger: Dict[str, Any]) -> bool:
    return idempotency_key in execution_ledger

def suppress_duplicate_execution(job_name: str, idempotency_key: str, execution_ledger: Dict[str, Any]) -> bool:
    return detect_duplicate_scheduled_run(idempotency_key, execution_ledger)
