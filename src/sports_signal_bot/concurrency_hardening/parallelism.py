import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    ParallelExecutionPlanRecord, ParallelLaneRecord, WorkerPoolRecord, QueueBudgetRecord,
    BackpressureRecord, ParallelJoinRecord, ParallelResultRecord, ParallelDeviationRecord,
    ParallelismHealthRecord, ParallelismManifestRecord, ParallelismWarningRecord
)

def build_parallel_execution_plan(
    plan_family: str,
    lane_count: int,
    worker_pool_size: int,
    queue_budget_items: int,
    join_strategy: str,
    max_parallelism: int,
    backpressure_policy: str
) -> ParallelExecutionPlanRecord:
    """Builds a ParallelExecutionPlanRecord."""
    plan_id = f"pep_{uuid.uuid4().hex[:8]}"

    warnings = []
    status = "plan_safe"

    if max_parallelism > 64: # Configurable threshold in real app
        status = "plan_overparallelized"
        warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"max_parallelism {max_parallelism} exceeds safety threshold.",
                severity="high"
            )
        )

    if worker_pool_size > max_parallelism:
        status = "plan_caveated"
        warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Worker pool size {worker_pool_size} is larger than max_parallelism {max_parallelism}.",
                severity="low"
            )
        )

    if plan_family not in [
        "bounded_preview_parallelism", "replay_probe_parallelism",
        "artifact_generation_parallelism", "trace_query_parallelism",
        "context_assembly_parallelism", "review_compilation_parallelism",
        "profiling_parallelism", "cache_invalidation_parallelism"
    ]:
         status = "plan_review_only"
         warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Unknown plan family: {plan_family}.",
                severity="medium"
            )
        )


    # Mock refs for simplicity
    lane_refs = [f"lane_{uuid.uuid4().hex[:8]}" for _ in range(lane_count)]
    pool_refs = [f"pool_{uuid.uuid4().hex[:8]}"]
    budget_refs = [f"budg_{uuid.uuid4().hex[:8]}"]
    join_refs = [f"join_{uuid.uuid4().hex[:8]}"]

    return ParallelExecutionPlanRecord(
        parallel_plan_id=plan_id,
        plan_family=plan_family,
        lane_refs=lane_refs,
        worker_pool_refs=pool_refs,
        queue_budget_refs=budget_refs,
        join_refs=join_refs,
        max_parallelism=max_parallelism,
        backpressure_policy_ref=f"bp_{uuid.uuid4().hex[:8]}",
        plan_status=status,
        warnings=warnings
    )


def assign_parallel_lanes(items: List[Any], plan: ParallelExecutionPlanRecord) -> Dict[str, List[Any]]:
    """Simulates assigning work to parallel lanes."""
    lanes = plan.lane_refs
    if not lanes:
        return {}

    assignments = {lane: [] for lane in lanes}
    for i, item in enumerate(items):
        assignments[lanes[i % len(lanes)]].append(item)
    return assignments


def enforce_parallelism_budgets(plan: ParallelExecutionPlanRecord, current_load: int) -> bool:
    """Checks if current load exceeds plan budgets."""
    if current_load > plan.max_parallelism:
        return False
    return True


def summarize_parallel_execution(plans: List[ParallelExecutionPlanRecord]) -> ParallelismManifestRecord:
    """Summarizes parallel execution plans into a manifest."""
    unhealthy_plans = [p.parallel_plan_id for p in plans if p.plan_status not in ["plan_safe", "plan_caveated"]]

    health = ParallelismHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(unhealthy_plans) == 0,
        status_summary=f"Found {len(unhealthy_plans)} unhealthy plans out of {len(plans)} total."
    )

    return ParallelismManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        plans=plans,
        health=health
    )
