from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import uuid

from .states import ControllerState, RefreshRiskLevel, ProblemClass
from .contracts import RefreshProblem, StateTransition, RefreshManifest
from .decisions import RefreshDecisionEngine
from .planning import RefreshPlanBuilder
from .executor import RefreshExecutor
from .validation import PostRefreshValidator
from .freeze import FreezeManager
from .degrade import DegradeManager
from .history import RefreshHistoryStore

class RefreshControllerRunner:
    def __init__(self, config=None):
        self.config = config or {}
        self.engine = RefreshDecisionEngine(self.config)
        self.executor = RefreshExecutor()
        self.validator = PostRefreshValidator()
        self.freeze_mgr = FreezeManager()
        self.degrade_mgr = DegradeManager()
        self.history = RefreshHistoryStore()

        self.current_state = ControllerState.HEALTHY

    def register_handler(self, family, handler):
        self.executor.register_handler(family, handler)

    def process_monitoring_output(self, monitor_output: dict, dry_run: bool = False) -> RefreshManifest:
        # 1. Classify problems
        problems = self.engine.classify_refresh_problem(monitor_output)

        if not problems:
            # Everything is fine, transition to healthy
            if self.current_state != ControllerState.HEALTHY:
                 self._transition(ControllerState.HEALTHY, "No problems detected")
                 self.freeze_mgr.release_freeze()
                 self.degrade_mgr.release_degrade()

            manifest = RefreshManifest(
                detected_problems=[],
                chosen_plan=None,
                attempt=None,
                state_transitions=[],
                current_state=self.current_state,
                freeze_record=self.freeze_mgr.get_current_freeze(),
                degrade_record=self.degrade_mgr.get_current_degrade()
            )
            return manifest

        # 2. Derive candidates & Build plan (we just take the first problem for simplicity in this MVP)
        primary_problem = problems[0]
        candidates = self.engine.derive_refresh_candidates(primary_problem)

        builder = RefreshPlanBuilder().set_problem(primary_problem)
        for c in candidates:
            builder.add_candidate(c)
        plan = builder.build()

        # 3. Transition to pending/review based on plan risk
        attempt = None
        if plan.blocked_reasons or plan.risk_level == RefreshRiskLevel.HIGH:
             self._transition(ControllerState.MANUAL_REVIEW_REQUIRED, "High risk plan requires review")
             self.freeze_mgr.activate_freeze(reason="Manual review required", scope="global")
        else:
             self._transition(ControllerState.REFRESH_PENDING, "Safe plan derived")

             # 4. Execute if not dry_run and safe
             if not dry_run:
                 self._transition(ControllerState.REFRESHING, "Starting execution")
                 attempt = self.executor.execute_plan(plan)

                 # 5. Validate
                 if attempt.status == "success":
                      self.validator.validate_refresh_outcome(attempt)

                 self.history.record_attempt(attempt)

                 # 6. Post-execution transition
                 new_state = self.engine.determine_state_transition(self.current_state, plan, attempt.status == "success" and attempt.validation_passed)
                 self._transition(new_state, f"Execution completed with status: {attempt.status}")

                 if new_state == ControllerState.FAILED_REFRESH:
                     self.freeze_mgr.activate_freeze(reason="Refresh failed", scope="global")
                     self._transition(ControllerState.FROZEN, "Frozen due to failed refresh")

        manifest = RefreshManifest(
            detected_problems=problems,
            chosen_plan=plan,
            attempt=attempt,
            state_transitions=self.history.transitions[-5:], # recent ones
            current_state=self.current_state,
            freeze_record=self.freeze_mgr.get_current_freeze(),
            degrade_record=self.degrade_mgr.get_current_degrade()
        )
        self.history.record_manifest(manifest)
        return manifest

    def _transition(self, to_state: ControllerState, reason: str):
        if self.current_state != to_state:
            t = StateTransition(
                 from_state=self.current_state,
                 to_state=to_state,
                 reason=reason
            )
            self.current_state = to_state
            self.history.record_transition(t)
