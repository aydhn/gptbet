from .contracts import RunbookRecord

def get_runbook(runbook_name: str) -> RunbookRecord:
    # Dummy implementation loading static profiles
    if runbook_name == "daily_live_like_pipeline":
        return RunbookRecord(
            runbook_name="daily_live_like_pipeline",
            purpose="Full daily suite",
            ordered_job_steps=["ingest", "inference", "dispatch", "monitoring"],
            normal_path=["ingest", "inference", "dispatch", "monitoring"],
            degraded_path=["ingest", "inference", "monitoring"],
            freeze_path=["monitoring"],
            operator_notes="Standard daily run",
            expected_outputs=["dispatch_manifest", "monitoring_manifest"],
            escalation_hints="Escalate to human if monitoring fails"
        )
    return RunbookRecord(
        runbook_name="default",
        purpose="Default run",
        ordered_job_steps=[],
        normal_path=[],
        degraded_path=[],
        freeze_path=[],
        operator_notes="",
        expected_outputs=[],
        escalation_hints=""
    )
