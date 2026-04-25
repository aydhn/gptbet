from typing import Any, Dict, List

from sports_signal_bot.research.contracts import (PeriodRunRecord,
                                                  ResearchScenario,
                                                  WindowDefinition)
from sports_signal_bot.research.windows import (
    decide_skip_or_degrade, validate_window_data_sufficiency)


class PeriodRunner:
    """Orchestrates a single walk-forward period."""

    def __init__(self, scenario: ResearchScenario):
        self.scenario = scenario

    def run_period(self, window: WindowDefinition) -> PeriodRunRecord:
        """
        Runs the full lifecycle for a period.
        In a real scenario, this would call:
        - DatasetAssembler
        - ModelTrainers
        - Calibrators
        - Ensembler
        - Stacker
        - Evaluator
        For this PR, we mock the counts and evaluation to prove the orchestrator.
        """

        # 1. Dataset assembly (Mocked)
        train_count = 150 if window.train_start else 0
        calibration_count = 50 if window.calibration_start else 0
        forward_count = 30

        suff_info = validate_window_data_sufficiency(
            window,
            train_count,
            calibration_count,
            forward_count,
            self.scenario.minimum_rows_guard,
        )

        decision = decide_skip_or_degrade(
            suff_info, self.scenario.skip_period_if_insufficient_data
        )

        warnings = []
        if decision == "skip":
            return PeriodRunRecord(
                period_id=window.period_id,
                scenario_id=self.scenario.scenario_id,
                window=window,
                status="skipped",
                warnings=[f"Skipped due to insufficient data: {suff_info['issues']}"],
            )
        elif decision == "proceed_with_warnings":
            warnings.append(f"Proceeding despite data issues: {suff_info['issues']}")

        # 2-5. Training & Refresh decisions
        retrained = []
        reused = []
        if window.should_retrain:
            retrained.extend(self.scenario.enabled_models)
        else:
            reused.extend(self.scenario.enabled_models)

        cal_status = "refreshed" if window.should_recalibrate else "reused"
        ens_status = "refreshed" if window.should_reensemble else "reused"
        stk_status = "refreshed" if window.should_refresh_stacker else "reused"

        # 6-7. Forward Evaluation (Mocked)
        eval_summary = {"num_events_evaluated": forward_count, "metrics_by_source": {}}

        # Mock some metrics
        for m in self.scenario.enabled_models:
            eval_summary["metrics_by_source"][m] = {"log_loss": 0.65, "accuracy": 0.55}

        eval_summary["metrics_by_source"]["ensemble"] = {
            "log_loss": 0.63,
            "accuracy": 0.57,
        }

        if self.scenario.stacker_refresh_frequency:
            eval_summary["metrics_by_source"]["stacker"] = {
                "log_loss": 0.62,
                "accuracy": 0.58,
            }

        return PeriodRunRecord(
            period_id=window.period_id,
            scenario_id=self.scenario.scenario_id,
            window=window,
            status="success",
            retrained_model_names=retrained,
            reused_model_names=reused,
            calibrator_refresh_status=cal_status,
            ensemble_refresh_status=ens_status,
            stacker_refresh_status=stk_status,
            evaluation_summary=eval_summary,
            warnings=warnings,
        )
