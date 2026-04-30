from typing import List, Dict, Any
from .contracts import TournamentMetricRecord, ObjectiveDirection

def extract_candidate_objectives(
    candidate_id: str,
    simulation_metrics: List[Dict[str, Any]],
    strategy_config: Dict[str, Any]
) -> List[TournamentMetricRecord]:
    """Extracts and normalizes objective metrics from raw simulation outputs."""
    metrics = []

    # Mapping of raw metric names to expected directions
    objective_directions = {
        "selected_subset_quality_delta": ObjectiveDirection.MAXIMIZE,
        "dispute_burden_delta": ObjectiveDirection.MINIMIZE,
        "review_queue_pressure_delta": ObjectiveDirection.MINIMIZE,
        "support_strength": ObjectiveDirection.MAXIMIZE,
        "estimated_release_risk": ObjectiveDirection.MINIMIZE,
        "materiality_score": ObjectiveDirection.MAXIMIZE,
        "scope_breadth": ObjectiveDirection.MINIMIZE,
        "simulation_confidence": ObjectiveDirection.MAXIMIZE,
        "decision_quality_delta": ObjectiveDirection.MAXIMIZE
    }

    # Override with strategy config if available
    if "objective_directions" in strategy_config:
        objective_directions.update({
            k: ObjectiveDirection(v)
            for k, v in strategy_config["objective_directions"].items()
        })

    for raw_metric in simulation_metrics:
        name = raw_metric.get("metric_name")
        value = raw_metric.get("value", 0.0)

        if name in objective_directions:
            direction = objective_directions[name]
            metrics.append(TournamentMetricRecord(
                metric_name=name,
                value=value,
                direction=direction
            ))

    return metrics

def build_objective_vector(
    metrics: List[TournamentMetricRecord],
    required_metrics: List[str]
) -> List[float]:
    """Builds a standardized objective vector for pareto comparisons.
    Missing metrics are padded with worst-case values based on direction.
    """
    vector = []
    metric_map = {m.metric_name: m for m in metrics}

    for req in required_metrics:
        if req in metric_map:
            m = metric_map[req]
            # Convert all to maximization problem for easier pareto math
            val = m.value if m.direction == ObjectiveDirection.MAXIMIZE else -m.value
            vector.append(val)
        else:
            # Missing metric penalty (negative infinity)
            vector.append(float('-inf'))

    return vector
