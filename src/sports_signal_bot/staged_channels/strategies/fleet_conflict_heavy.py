from sports_signal_bot.staged_channels.strategies.base import BaseStagedChannelStrategy
from sports_signal_bot.staged_channels.contracts import StageStatus

class FleetAwareConflictHeavyStrategy(BaseStagedChannelStrategy):
    def evaluate_progression(self, candidate_id: str, current_stage: str, metrics: dict) -> str:
        if metrics.get("conflict_count", 0) > 0:
            return StageStatus.ROLLOUT_HOLD.value
        return "progress"

    def handle_fleet_conflicts(self, fleet, candidate_id: str) -> bool:
        # Strictly reject any candidate that causes a fleet conflict
        return False
