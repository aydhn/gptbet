import datetime
from typing import Any, Dict, Optional

from sports_signal_bot.research.contracts import ResearchScenario


class ResearchScenarioLoader:
    """Loads and validates research scenarios from configuration."""

    @staticmethod
    def load_from_config(
        config: Dict[str, Any], scenario_id: str = "custom"
    ) -> ResearchScenario:
        """
        Creates a ResearchScenario from a configuration dictionary.
        """
        # Convert string dates to datetime.date if needed
        start_date = config.get("start_date")
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

        end_date = config.get("end_date")
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        return ResearchScenario(
            scenario_id=config.get("scenario_id", scenario_id),
            sport=config.get("sport", "football"),
            market_type=config.get("market_type", "1x2"),
            start_date=start_date
            or (datetime.date.today() - datetime.timedelta(days=365)),
            end_date=end_date or datetime.date.today(),
            planning_mode=config.get("planning_mode", "expanding"),
            initial_train_window_days=config.get("initial_train_window_days", 180),
            calibration_window_days=config.get("calibration_window_days", 30),
            forward_test_window_days=config.get("forward_test_window_days", 30),
            retrain_frequency=config.get("retrain_frequency", 1),
            recalibration_frequency=config.get("recalibration_frequency", 1),
            reensemble_frequency=config.get("reensemble_frequency", 1),
            stacker_refresh_frequency=config.get("stacker_refresh_frequency"),
            minimum_rows_guard=config.get("minimum_rows_guard", 100),
            skip_period_if_insufficient_data=config.get(
                "skip_period_if_insufficient_data", True
            ),
            enabled_sources=config.get("enabled_sources", []),
            enabled_models=config.get("enabled_models", []),
            monthly_reporting_enabled=config.get("monthly_reporting_enabled", True),
        )
