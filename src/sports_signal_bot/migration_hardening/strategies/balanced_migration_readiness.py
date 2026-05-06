from typing import Dict, Any
from .base import BaseMigrationHardeningStrategy
from ..migration_lanes import LaneStatus

class BalancedMigrationReadinessStrategy(BaseMigrationHardeningStrategy):
    """
    practical coordination and migration coverage with strict honesty contracts
    """
    def evaluate_migration_readiness(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lane = context.get('lane')
        if not lane: return {"status": "error"}
        return {
            "strategy": "Balanced",
            "is_release_blocking": lane.lane_status == LaneStatus.migration_blocked,
            "lane_status": lane.lane_status.value
        }

    def evaluate_coordination(self, context: Dict[str, Any]) -> Dict[str, Any]:
        drill = context.get('drill')
        return {
            "strategy": "Balanced",
            "is_release_blocking": False, # Tolerates some gaps if honest
            "drill_status": drill.readiness_status.value if drill else "unknown"
        }

    def evaluate_recovery_chain(self, context: Dict[str, Any]) -> Dict[str, Any]:
        chain = context.get('chain')
        return {
             "strategy": "Balanced",
             "is_release_blocking": chain.chain_status == "chain_broken" if chain else True,
             "chain_status": chain.chain_status.value if chain else "unknown"
        }

    def evaluate_visibility_wargame(self, context: Dict[str, Any]) -> Dict[str, Any]:
         game = context.get('game')
         return {
             "strategy": "Balanced",
             "is_release_blocking": any(l.is_critical for l in game.loss_refs) if game else True,
             "war_game_status": game.war_game_status.value if game else "unknown"
         }
