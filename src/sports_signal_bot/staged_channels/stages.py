import datetime
import uuid
from typing import Dict, Any, List
from sports_signal_bot.staged_channels.contracts import RolloutStageRecord, StageStatus

def evaluate_shadow_exit(stage_record: RolloutStageRecord) -> Dict[str, Any]:
    # Placeholder logic
    return {
        "pass": True,
        "failures": []
    }

def evaluate_candidate_eval_exit(stage_record: RolloutStageRecord) -> Dict[str, Any]:
    # Placeholder logic
    return {
        "pass": True,
        "failures": []
    }

def evaluate_live_like_safe_exit(stage_record: RolloutStageRecord) -> Dict[str, Any]:
    # Placeholder logic
    return {
        "pass": True,
        "failures": []
    }

def summarize_exit_failures(exit_result: Dict[str, Any]) -> List[str]:
    return exit_result.get("failures", [])

def summarize_stage_evaluation_requirements(status: StageStatus) -> List[str]:
    if status in [StageStatus.RUNNING_IN_SHADOW, StageStatus.SHADOW_VERIFIED]:
        return ["no critical safety regression", "no unfair comparison", "evidence bundle complete"]
    elif status in [StageStatus.RUNNING_CANDIDATE_EVAL, StageStatus.CANDIDATE_EVAL_VERIFIED]:
        return ["required gates valid", "no blocking fleet conflict"]
    elif status in [StageStatus.RUNNING_LIVE_LIKE_SAFE, StageStatus.LIVE_LIKE_SAFE_VERIFIED]:
        return ["ops risk acceptable", "release-blocking concerns absent", "promote recommendation possible"]
    return []

def trace_candidate_stage_path(candidate_id: str, history: List[RolloutStageRecord]) -> List[StageStatus]:
    return [record.stage_status for record in history if record.candidate_release_id == candidate_id]

def rollback_candidate_to_shadow(candidate_id: str) -> RolloutStageRecord:
    return RolloutStageRecord(
        stage_id=str(uuid.uuid4()),
        candidate_release_id=candidate_id,
        current_channel="shadow_candidate_channel",
        stage_status=StageStatus.ROLLBACK_TO_SHADOW,
        entered_at=datetime.datetime.now(datetime.timezone.utc),
    )
