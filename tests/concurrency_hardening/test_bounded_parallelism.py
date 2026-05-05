import pytest
from sports_signal_bot.concurrency_hardening.parallelism import build_parallel_execution_plan

def test_build_parallel_plan_safe():
    plan = build_parallel_execution_plan(
        plan_family="bounded_preview_parallelism",
        lane_count=4,
        worker_pool_size=4,
        queue_budget_items=100,
        join_strategy="wait_all",
        max_parallelism=16,
        backpressure_policy="drop"
    )
    assert plan.plan_status == "plan_safe"

def test_build_parallel_plan_overparallelized():
    plan = build_parallel_execution_plan(
        plan_family="bounded_preview_parallelism",
        lane_count=4,
        worker_pool_size=4,
        queue_budget_items=100,
        join_strategy="wait_all",
        max_parallelism=128, # > 64 threshold
        backpressure_policy="drop"
    )
    assert plan.plan_status == "plan_overparallelized"
