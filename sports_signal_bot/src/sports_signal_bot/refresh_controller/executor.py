from typing import Dict, Any, Callable
from datetime import datetime, timezone
from .contracts import RefreshPlan, RefreshAttempt, RefreshAction
from .states import RefreshActionFamily

class RefreshExecutor:
    def __init__(self):
        self.handlers: Dict[RefreshActionFamily, Callable[[RefreshAction], bool]] = {}

    def register_handler(self, family: RefreshActionFamily, handler: Callable[[RefreshAction], bool]):
        self.handlers[family] = handler

    def execute_plan(self, plan: RefreshPlan) -> RefreshAttempt:
        attempt = RefreshAttempt(plan_id=plan.plan_id)

        if plan.blocked_reasons:
             attempt.status = "skipped"
             attempt.completed_at = datetime.now(timezone.utc)
             attempt.errors.extend(plan.blocked_reasons)
             return attempt

        all_success = True
        for step in plan.steps:
            action = step.action
            if action.family in self.handlers:
                try:
                    success = self.handlers[action.family](action)
                    if success:
                        attempt.executed_actions.append(action.action_id)
                    else:
                        all_success = False
                        attempt.errors.append(f"Step {step.step_order} failed.")
                        break # Stop on first failure
                except Exception as e:
                    all_success = False
                    attempt.errors.append(f"Step {step.step_order} exception: {str(e)}")
                    break
            else:
                 all_success = False
                 attempt.errors.append(f"No handler for {action.family}")
                 break

        attempt.status = "success" if all_success else "failed"
        attempt.completed_at = datetime.now(timezone.utc)
        return attempt
