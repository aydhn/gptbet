from typing import List, Optional
from datetime import datetime

from .states import ProblemClass, RefreshRiskLevel, RefreshActionFamily, ControllerState
from .contracts import RefreshProblem, RefreshAction, RefreshPlan, RefreshPlanStep

class RefreshDecisionEngine:
    def __init__(self, config=None):
        self.config = config or {}

    def classify_refresh_problem(self, monitor_output: dict) -> List[RefreshProblem]:
        problems = []
        # Basic mapping logic placeholder
        if monitor_output.get("stale_artifact_count", 0) > 0:
            problems.append(RefreshProblem(
                problem_class=ProblemClass.ARTIFACT_FRESHNESS,
                severity="high",
                component="artifacts",
                description="Stale artifacts detected"
            ))
        if monitor_output.get("data_delay_seconds", 0) > 3600:
            problems.append(RefreshProblem(
                problem_class=ProblemClass.DATA_FRESHNESS,
                severity="medium",
                component="data",
                description="Data delay exceeds threshold"
            ))
        if not problems and monitor_output.get("global_health_score", 1.0) < 0.8:
            problems.append(RefreshProblem(
                 problem_class=ProblemClass.RUNTIME_PIPELINE,
                 severity="low",
                 component="pipeline",
                 description="Global health score below threshold"
            ))
        return problems

    def derive_refresh_candidates(self, problem: RefreshProblem) -> List[RefreshAction]:
        candidates = []
        if problem.problem_class == ProblemClass.ARTIFACT_FRESHNESS:
            candidates.append(self._build_action(RefreshActionFamily.CATALOG_REFRESH, RefreshRiskLevel.LOW, True, False))
            candidates.append(self._build_action(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, RefreshRiskLevel.LOW, True, False))
        elif problem.problem_class == ProblemClass.DATA_FRESHNESS:
            candidates.append(self._build_action(RefreshActionFamily.SNAPSHOT_RESELECTION, RefreshRiskLevel.LOW, True, False))
        elif problem.problem_class == ProblemClass.RUNTIME_PIPELINE:
            candidates.append(self._build_action(RefreshActionFamily.ENABLE_SAFE_FALLBACK_MODE, RefreshRiskLevel.LOW, True, False))

        # Add high risk fallback just in case
        # candidates.append(self._build_action(RefreshActionFamily.RETRAIN_MODEL, RefreshRiskLevel.HIGH, False, True))
        return candidates

    def score_refresh_action_risk(self, action: RefreshAction) -> RefreshRiskLevel:
        return action.risk_level

    def select_safe_refresh_plan(self, problem: RefreshProblem, candidates: List[RefreshAction]) -> RefreshPlan:
        steps = []
        for i, action in enumerate(candidates):
             if action.auto_execute_allowed:
                 steps.append(RefreshPlanStep(step_order=i+1, action=action, expected_outcome="executed"))
             elif action.requires_manual_review:
                  pass # Skip high risk for auto plan

        risk_level = RefreshRiskLevel.LOW if all(s.action.risk_level == RefreshRiskLevel.LOW for s in steps) else RefreshRiskLevel.MEDIUM
        if not steps:
            risk_level = RefreshRiskLevel.HIGH

        blocked_reasons = []
        if risk_level == RefreshRiskLevel.HIGH:
            blocked_reasons.append("No safe auto-actions available.")

        return RefreshPlan(
            problem_id=problem.problem_id,
            steps=steps,
            risk_level=risk_level,
            blocked_reasons=blocked_reasons
        )

    def determine_state_transition(self, current_state: ControllerState, plan: RefreshPlan, execution_success: bool = None) -> ControllerState:
        if execution_success is True:
            return ControllerState.REFRESHED
        elif execution_success is False:
            return ControllerState.FAILED_REFRESH

        if plan.risk_level == RefreshRiskLevel.HIGH or plan.blocked_reasons:
             return ControllerState.MANUAL_REVIEW_REQUIRED

        if current_state in (ControllerState.HEALTHY, ControllerState.DEGRADED):
            return ControllerState.REFRESH_PENDING

        return current_state

    def _build_action(self, family: RefreshActionFamily, risk: RefreshRiskLevel, auto_exec: bool, manual: bool) -> RefreshAction:
        return RefreshAction(
            family=family,
            risk_level=risk,
            auto_execute_allowed=auto_exec,
            requires_manual_review=manual,
            reversible=True
        )
