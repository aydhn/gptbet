import datetime
from typing import List
from .contracts import (
    ExecutionLaneRuntimeRecord, RuntimeWindowRecord, RuntimeStatus,
    RuntimeStepRecord, StepStatus
)

def build_runtime_window(start: str, end: str) -> RuntimeWindowRecord:
    return RuntimeWindowRecord(
        start_time=start,
        end_time=end,
        max_duration_sec=3600,
        allowed_step_count=10,
        allowed_step_families=["refresh_freshness_metadata_step"],
        pause_allowance_sec=300,
        renewal_allowed=True,
        rollback_window_sec=1800,
        closure_verification_window_sec=600
    )

def init_runtime(lane_ref: str, token_ref: str, window: RuntimeWindowRecord) -> ExecutionLaneRuntimeRecord:
    return ExecutionLaneRuntimeRecord(
        runtime_id=f"rt_{lane_ref}",
        lane_ref=lane_ref,
        token_ref=token_ref,
        runtime_window=window,
        runtime_status=RuntimeStatus.READY
    )

def execute_step(runtime: ExecutionLaneRuntimeRecord, step: RuntimeStepRecord) -> bool:
    if runtime.runtime_status != RuntimeStatus.READY and runtime.runtime_status != RuntimeStatus.EXECUTING:
        return False
    step.actual_start = datetime.datetime.now().isoformat()
    step.step_status = StepStatus.EXECUTING
    runtime.runtime_status = RuntimeStatus.EXECUTING
    # simulate execution
    step.actual_end = datetime.datetime.now().isoformat()
    step.step_status = StepStatus.EXECUTED
    runtime.observed_checkpoints.extend(step.post_step_checkpoints)
    return True
