from typing import Dict, Any, List, Optional
from .contracts import ThresholdCandidateRecord

class ObjectiveEvaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.objective_name = config.get("objective_name", "precision_oriented")

    def evaluate(self, candidate: ThresholdCandidateRecord, metrics: Dict[str, float]) -> float:
        # Lower objective value is typically better, or we can maximize. Let's maximize.

        if self.objective_name == "precision_oriented":
            return metrics.get("accuracy", 0.0)

        elif self.objective_name == "probabilistic_quality":
            # Maximize negative log loss (or minimize log loss)
            log_loss = metrics.get("log_loss", float('inf'))
            return -log_loss if log_loss != float('inf') else -999.0

        elif self.objective_name == "balanced":
            weight_quality = self.config.get("weight_quality", 0.7)
            weight_coverage = self.config.get("weight_coverage", 0.3)
            acc = metrics.get("accuracy", 0.0)
            cov = candidate.coverage_rate
            return (weight_quality * acc) + (weight_coverage * cov)

        elif self.objective_name == "edge_aware":
            avg_edge = metrics.get("average_edge", 0.0)
            acc = metrics.get("accuracy", 0.0)
            return (acc * 0.5) + (avg_edge * 0.5)

        elif self.objective_name == "conservative":
            acc = metrics.get("accuracy", 0.0)
            unc = metrics.get("average_uncertainty_penalty", 1.0)
            return acc - (unc * 0.5)

        return metrics.get("accuracy", 0.0)
