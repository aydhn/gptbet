from typing import Dict, Any
from .base import BaseMigrationHardeningStrategy
from ..migration_lanes import LaneStatus
from ..team_coordination import ReadinessStatus
from ..recovery_chains import ChainStatus
from ..visibility_wargames import WarGameStatus

class ConservativeMigrationHardeningStrategy(BaseMigrationHardeningStrategy):
    """
    Default conservative strategy:
    - slightest handoff or visibility gap visible
    - stale source rejection strict
    - strong release blocking
    """
    def evaluate_migration_readiness(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lane = context.get('lane')
        if not lane: return {"status": "error"}
        is_blocked = lane.lane_status in [LaneStatus.migration_blocked, LaneStatus.migration_gapped]
        return {
            "strategy": "Conservative",
            "is_release_blocking": is_blocked or len(lane.residue_refs) > 0,
            "lane_status": lane.lane_status.value
        }

    def evaluate_coordination(self, context: Dict[str, Any]) -> Dict[str, Any]:
        drill = context.get('drill')
        if not drill: return {"status": "error"}
        return {
            "strategy": "Conservative",
            "is_release_blocking": drill.readiness_status != ReadinessStatus.coordination_verified,
            "drill_status": drill.readiness_status.value
        }

    def evaluate_recovery_chain(self, context: Dict[str, Any]) -> Dict[str, Any]:
        chain = context.get('chain')
        if not chain: return {"status": "error"}
        return {
            "strategy": "Conservative",
            "is_release_blocking": chain.chain_status in [ChainStatus.chain_broken, ChainStatus.chain_gapped],
            "chain_status": chain.chain_status.value
        }

    def evaluate_visibility_wargame(self, context: Dict[str, Any]) -> Dict[str, Any]:
        game = context.get('game')
        if not game: return {"status": "error"}
        has_critical = any(l.is_critical for l in game.loss_refs)
        return {
            "strategy": "Conservative",
            "is_release_blocking": has_critical or game.war_game_status == WarGameStatus.visibility_lost,
            "war_game_status": game.war_game_status.value
        }
