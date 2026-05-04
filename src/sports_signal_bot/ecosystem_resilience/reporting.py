import json

def get_kpi_metrics(overlay_score: float, mesh_success: float) -> dict:
    return {
        "trust_overlay_stability_score": overlay_score,
        "mesh_route_bounded_success_rate": mesh_success,
        "mesh_degraded_route_rate": 1.0 - mesh_success,
        "baseline_signal_relevance_rate": 0.85,
        "baseline_signal_staleness_rate": 0.15,
        "ecosystem_resilience_controller_action_rate": 0.05,
        "participant_overlay_fitness_rate": 0.90,
        "federated_currentness_conflict_rate": 0.02,
        "hub_mesh_pressure_index": 0.1,
        "sovereign_ecosystem_resilience_index": overlay_score * 0.9
    }

def generate_health_report(kpis: dict, dest: str):
    with open(dest, "w") as f:
        json.dump(kpis, f, indent=2)
