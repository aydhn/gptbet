import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    ParallelExecutionPlanConfig, ParallelExecutionPlanRecord,
    ParallelismHealthRecord, ParallelismManifestRecord,
    ParallelismWarningRecord
)


def _check_max_parallelism(
    config: ParallelExecutionPlanConfig,
    warnings: List[ParallelismWarningRecord]
) -> str:
    if config.max_parallelism > 64:  # Configurable threshold in real app
        warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"max_parallelism {config.max_parallelism} "
                        "exceeds safety threshold.",
                severity="high"
            )
        )
        return "plan_overparallelized"
    return "plan_safe"


def _check_worker_pool_size(
    config: ParallelExecutionPlanConfig,
    warnings: List[ParallelismWarningRecord]
) -> str:
    if config.worker_pool_size > config.max_parallelism:
        warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Worker pool size {config.worker_pool_size} "
                        f"is larger than max_parallelism "
                        f"{config.max_parallelism}.",
                severity="low"
            )
        )
        return "plan_caveated"
    return "plan_safe"


def _check_plan_family(
    config: ParallelExecutionPlanConfig,
    warnings: List[ParallelismWarningRecord]
) -> str:
    if config.plan_family not in [
        "bounded_preview_parallelism", "replay_probe_parallelism",
        "artifact_generation_parallelism", "trace_query_parallelism",
        "context_assembly_parallelism", "review_compilation_parallelism",
        "profiling_parallelism", "cache_invalidation_parallelism"
    ]:
        warnings.append(
            ParallelismWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Unknown plan family: {config.plan_family}.",
                severity="medium"
            )
        )
        return "plan_review_only"
    return "plan_safe"


def build_parallel_execution_plan(
    config: ParallelExecutionPlanConfig
) -> ParallelExecutionPlanRecord:
    """Builds a ParallelExecutionPlanRecord."""
    plan_id = f"pep_{uuid.uuid4().hex[:8]}"

    warnings = []

    status = "plan_safe"

    max_status = _check_max_parallelism(config, warnings)
    if max_status != "plan_safe":
        status = max_status

    pool_status = _check_worker_pool_size(config, warnings)
    if pool_status != "plan_safe":
        status = pool_status

    family_status = _check_plan_family(config, warnings)
    if family_status != "plan_safe":
        status = family_status

    # Mock refs for simplicity
    lane_refs = [
        f"lane_{uuid.uuid4().hex[:8]}" for _ in range(config.lane_count)
    ]
    pool_refs = [f"pool_{uuid.uuid4().hex[:8]}"]
    budget_refs = [f"budg_{uuid.uuid4().hex[:8]}"]
    join_refs = [f"join_{uuid.uuid4().hex[:8]}"]

    return ParallelExecutionPlanRecord(
        parallel_plan_id=plan_id,
        plan_family=config.plan_family,
        lane_refs=lane_refs,
        worker_pool_refs=pool_refs,
        queue_budget_refs=budget_refs,
        join_refs=join_refs,
        max_parallelism=config.max_parallelism,
        backpressure_policy_ref=f"bp_{uuid.uuid4().hex[:8]}",
        plan_status=status,
        warnings=warnings
    )


def assign_parallel_lanes(
    items: List[Any], plan: ParallelExecutionPlanRecord
) -> Dict[str, List[Any]]:
    """Simulates assigning work to parallel lanes."""
    lanes = plan.lane_refs
    if not lanes:
        return {}

    assignments = {lane: [] for lane in lanes}
    for i, item in enumerate(items):
        assignments[lanes[i % len(lanes)]].append(item)
    return assignments


def enforce_parallelism_budgets(
    plan: ParallelExecutionPlanRecord, current_load: int
) -> bool:
    """Checks if current load exceeds plan budgets."""
    if current_load > plan.max_parallelism:
        return False
    return True


def summarize_parallel_execution(
    plans: List[ParallelExecutionPlanRecord]
) -> ParallelismManifestRecord:
    """Summarizes parallel execution plans into a manifest."""
    unhealthy_plans = [
        p.parallel_plan_id for p in plans
        if p.plan_status not in ["plan_safe", "plan_caveated"]
    ]

    health = ParallelismHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(unhealthy_plans) == 0,
        status_summary=f"Found {len(unhealthy_plans)} unhealthy plans "
                       f"out of {len(plans)} total."
    )

    return ParallelismManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        plans=plans,
        health=health
    )
