import datetime
from typing import List

from sports_signal_bot.research.contracts import (ResearchScenario,
                                                  WalkForwardPlan,
                                                  WindowDefinition)
from sports_signal_bot.research.policies import RefreshPolicyResolver


class WalkForwardPlanner:
    """Generates WalkForwardPlan from ResearchScenario."""

    def __init__(self, scenario: ResearchScenario):
        self.scenario = scenario
        self.policy_resolver = RefreshPolicyResolver(scenario)

    def generate_plan(self) -> WalkForwardPlan:
        """Generates the plan."""
        periods = []
        period_id = 1

        current_forward_start = self.scenario.start_date + datetime.timedelta(
            days=self.scenario.initial_train_window_days
        )

        # If calibration is used, shift forward start further
        if self.scenario.calibration_window_days:
            current_forward_start += datetime.timedelta(
                days=self.scenario.calibration_window_days
            )

        while current_forward_start < self.scenario.end_date:
            forward_end = min(
                current_forward_start
                + datetime.timedelta(days=self.scenario.forward_test_window_days - 1),
                self.scenario.end_date,
            )

            # Determine train start based on planning mode
            if self.scenario.planning_mode == "rolling":
                train_start = current_forward_start - datetime.timedelta(
                    days=self.scenario.initial_train_window_days
                    + (self.scenario.calibration_window_days or 0)
                )
            else:  # expanding, anchored, fixed
                train_start = self.scenario.start_date

            train_end = current_forward_start - datetime.timedelta(
                days=(self.scenario.calibration_window_days or 0) + 1
            )

            calibration_start = None
            calibration_end = None
            if self.scenario.calibration_window_days:
                calibration_start = train_end + datetime.timedelta(days=1)
                calibration_end = current_forward_start - datetime.timedelta(days=1)

            # Determine refresh flags
            should_retrain = self.policy_resolver.should_retrain_model(period_id)
            should_recalibrate = self.policy_resolver.should_recalibrate(period_id)
            should_reensemble = self.policy_resolver.should_refresh_ensemble(
                period_id, should_recalibrate
            )
            should_refresh_stacker = self.policy_resolver.should_refresh_stacker(
                period_id
            )

            window = WindowDefinition(
                period_id=period_id,
                train_start=train_start,
                train_end=train_end,
                calibration_start=calibration_start,
                calibration_end=calibration_end,
                forward_start=current_forward_start,
                forward_end=forward_end,
                should_retrain=should_retrain,
                should_recalibrate=should_recalibrate,
                should_reensemble=should_reensemble,
                should_refresh_stacker=should_refresh_stacker,
            )
            periods.append(window)

            # Advance
            current_forward_start = forward_end + datetime.timedelta(days=1)
            period_id += 1

        return WalkForwardPlan(
            scenario_id=self.scenario.scenario_id,
            sport=self.scenario.sport,
            market_type=self.scenario.market_type,
            periods=periods,
            total_periods=len(periods),
            planning_mode=self.scenario.planning_mode,
        )
