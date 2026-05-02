from datetime import datetime, timezone
from typing import List
from src.sports_signal_bot.resilience_fabric.contracts import GameDaySimulationRecord, ResilienceScorecardRecord

def enter_simulation_mode(scenario_family: str) -> str:
    print(f"ENTERING SIMULATION ISOLATION: {scenario_family}")
    return "simulation_active"

def exit_simulation_mode(context: str) -> str:
    print(f"EXITING SIMULATION ISOLATION")
    return "live"

def build_game_day_scenario(sim_id: str, family: str, injected: List[str]) -> GameDaySimulationRecord:
    return GameDaySimulationRecord(
        simulation_id=sim_id,
        scenario_family=family,
        target_scope="system",
        injected_failures=injected,
        expected_behaviors=["degraded_mode_triggered", "no_safe_route_visible"],
        observed_behaviors=["degraded_mode_triggered", "no_safe_route_visible"],
        resilience_score=0.85,
        remediation_refs=[]
    )

def compute_resilience_scorecard(simulations: List[GameDaySimulationRecord]) -> ResilienceScorecardRecord:
    # Mock computation
    avg_score = sum(s.resilience_score for s in simulations) / len(simulations) if simulations else 0
    band = "strong" if avg_score > 0.8 else "acceptable"

    return ResilienceScorecardRecord(
        scorecard_id="scorecard_current",
        timestamp=datetime.now(timezone.utc),
        overall_band=band,
        dimensions={
            "sync_recovery_time": 0.9,
            "route_degradation_containment": 0.8,
            "no_safe_route_visibility": 0.85
        }
    )
