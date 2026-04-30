from sports_signal_bot.staged_channels.strategies.base import BaseStagedChannelStrategy
from sports_signal_bot.staged_channels.contracts import StageStatus

class ConservativeStagedChannelStrategy(BaseStagedChannelStrategy):
    def evaluate_progression(self, candidate_id: str, current_stage: str, metrics: dict) -> str:
        # Conservative: stay in shadow longer
        if current_stage == StageStatus.RUNNING_IN_SHADOW.value:
            if metrics.get("days_in_shadow", 0) < 7:
                return StageStatus.RUNNING_IN_SHADOW.value
            return StageStatus.SHADOW_VERIFIED.value
        return current_stage # Default hold

    def handle_fleet_conflicts(self, fleet, candidate_id: str) -> bool:
        return False # Extremely cautious, reject if ANY conflict is suspected (mock logic)
