import pytest
from sports_signal_bot.refresh_controller.planning import RefreshPlanBuilder
from sports_signal_bot.refresh_controller.contracts import RefreshAction, RefreshProblem
from sports_signal_bot.refresh_controller.states import RefreshActionFamily, RefreshRiskLevel, ProblemClass

def test_refresh_plan_builder():
    problem = RefreshProblem(
        problem_class=ProblemClass.ARTIFACT_FRESHNESS,
        severity="medium",
        component="artifact",
        description="test"
    )

    action1 = RefreshAction(
        family=RefreshActionFamily.CATALOG_REFRESH,
        risk_level=RefreshRiskLevel.LOW,
        auto_execute_allowed=True,
        requires_manual_review=False,
        reversible=True
    )

    action2 = RefreshAction(
        family=RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION,
        risk_level=RefreshRiskLevel.LOW,
        auto_execute_allowed=True,
        requires_manual_review=False,
        reversible=True
    )

    builder = RefreshPlanBuilder().set_problem(problem)
    builder.add_candidate(action1).add_candidate(action2)

    plan = builder.build()

    assert plan.problem_id == problem.problem_id
    assert len(plan.steps) == 2
    assert plan.risk_level == RefreshRiskLevel.LOW
    assert len(plan.blocked_reasons) == 0

def test_refresh_plan_builder_blocked():
    problem = RefreshProblem(
        problem_class=ProblemClass.ARTIFACT_FRESHNESS,
        severity="medium",
        component="artifact",
        description="test"
    )

    action = RefreshAction(
        family=RefreshActionFamily.RETRAIN_MODEL,
        risk_level=RefreshRiskLevel.HIGH,
        auto_execute_allowed=False,
        requires_manual_review=True,
        reversible=False
    )

    builder = RefreshPlanBuilder().set_problem(problem)
    builder.add_candidate(action)

    plan = builder.build()

    assert plan.problem_id == problem.problem_id
    assert len(plan.steps) == 0 # High risk action skips step creation
    assert plan.risk_level == RefreshRiskLevel.HIGH
    assert len(plan.blocked_reasons) > 0
