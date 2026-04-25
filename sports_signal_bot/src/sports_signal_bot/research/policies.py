from sports_signal_bot.research.contracts import ResearchScenario


class RefreshPolicyResolver:
    """Resolves refresh policies based on the research scenario config."""

    def __init__(self, scenario: ResearchScenario):
        self.scenario = scenario

    def should_retrain_model(self, period_id: int) -> bool:
        """Determines if base models should be retrained this period."""
        if self.scenario.retrain_frequency <= 0:
            return False  # Never retrain
        return period_id == 1 or (period_id - 1) % self.scenario.retrain_frequency == 0

    def should_recalibrate(self, period_id: int) -> bool:
        """Determines if calibration layers should be retrained."""
        if self.scenario.recalibration_frequency <= 0:
            return False
        return (
            period_id == 1
            or (period_id - 1) % self.scenario.recalibration_frequency == 0
        )

    def should_refresh_ensemble(self, period_id: int, recalibrated: bool) -> bool:
        """Determines if ensemble should be refreshed."""
        # Often refresh ensemble if underlying models recalibrated
        if recalibrated:
            return True

        if self.scenario.reensemble_frequency <= 0:
            return False
        return (
            period_id == 1 or (period_id - 1) % self.scenario.reensemble_frequency == 0
        )

    def should_refresh_stacker(self, period_id: int) -> bool:
        """Determines if meta-stacker should be retrained."""
        freq = self.scenario.stacker_refresh_frequency
        if freq is None or freq <= 0:
            return False
        return period_id == 1 or (period_id - 1) % freq == 0
