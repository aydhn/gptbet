from sports_signal_bot.staged_channels.strategies.base import BaseStagedChannelStrategy

class FastSafeCandidateWaveStrategy(BaseStagedChannelStrategy):
    def evaluate_progression(self, candidate_id: str, current_stage: str, metrics: dict) -> str:
        if metrics.get("risk_level") == "low":
            return "progress_fast"
        return "hold"

    def handle_fleet_conflicts(self, fleet, candidate_id: str) -> bool:
        return True # Assumes narrow patches don't conflict easily
