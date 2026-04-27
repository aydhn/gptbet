from typing import List, Optional
from .contracts import RefreshAction, RefreshPlan, RefreshPlanStep, RefreshProblem
from .states import RefreshRiskLevel

class RefreshPlanBuilder:
    def __init__(self):
        self.candidates: List[RefreshAction] = []
        self.problem_id: Optional[str] = None

    def set_problem(self, problem: RefreshProblem):
        self.problem_id = problem.problem_id
        return self

    def add_candidate(self, action: RefreshAction):
        self.candidates.append(action)
        return self

    def build(self) -> RefreshPlan:
        steps = []
        order = 1
        blocked = []
        highest_risk = RefreshRiskLevel.LOW

        for action in self.candidates:
            if action.risk_level == RefreshRiskLevel.HIGH:
                highest_risk = RefreshRiskLevel.HIGH
                blocked.append(f"Action {action.family} requires manual review.")
                continue

            if action.risk_level == RefreshRiskLevel.MEDIUM:
                highest_risk = RefreshRiskLevel.MEDIUM if highest_risk == RefreshRiskLevel.LOW else highest_risk

            steps.append(RefreshPlanStep(
                step_order=order,
                action=action,
                expected_outcome="expected success"
            ))
            order += 1

        if not steps and self.candidates:
             blocked.append("No executable steps in plan.")

        return RefreshPlan(
            problem_id=self.problem_id or "unknown",
            steps=steps,
            risk_level=highest_risk,
            blocked_reasons=blocked
        )
