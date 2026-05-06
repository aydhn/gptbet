from typing import Dict, Any, List
from .contracts import RunbookRehearsalRecord, RunbookRecord, RehearsalMismatchRecord

def run_runbook_rehearsal(runbook: RunbookRecord) -> RunbookRehearsalRecord:
    return RunbookRehearsalRecord(
        rehearsal_id="rehearsal_" + runbook.runbook_id,
        runbook_ref=runbook.runbook_id,
        status="completed"
    )

def compare_rehearsal_to_runbook(rehearsal: RunbookRehearsalRecord, runbook: RunbookRecord) -> List[RehearsalMismatchRecord]:
    return []

def summarize_runbook_rehearsal(rehearsal: RunbookRehearsalRecord) -> Dict[str, Any]:
    return {"rehearsal_id": rehearsal.rehearsal_id, "status": rehearsal.status}
