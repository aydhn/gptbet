import datetime
from sports_signal_bot.staged_channels.contracts import RolloutStageRecord, StageStatus

def build_rollout_evidence_packet(candidate_id: str, stage_record: RolloutStageRecord, metrics: dict) -> dict:
    return {
        "candidate_id": candidate_id,
        "stage": stage_record.stage_status.value,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metrics": metrics,
        "explanation": "Evidence collected during rollout stage."
    }

def explain_stage_transition(old_stage: StageStatus, new_stage: StageStatus, reason: str) -> str:
    return f"Transitioned from {old_stage.value} to {new_stage.value} because {reason}."
