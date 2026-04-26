from typing import Any, Dict, List

from .contracts import ThresholdCandidateRecord


class ConstraintEvaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def check_constraints(
        self, candidate: ThresholdCandidateRecord, metrics: Dict[str, float]
    ) -> bool:
        min_accepted = self.config.get("minimum_accepted_count", 0)
        if candidate.accepted_count < min_accepted:
            candidate.warnings.append(
                f"Failed constraint: min_accepted_count ({candidate.accepted_count} < {min_accepted})"
            )
            return False

        min_coverage = self.config.get("minimum_coverage_rate", 0.0)
        if candidate.coverage_rate < min_coverage:
            candidate.warnings.append(
                f"Failed constraint: min_coverage_rate ({candidate.coverage_rate} < {min_coverage})"
            )
            return False

        max_uncertainty = self.config.get("maximum_average_uncertainty", 1.0)
        if candidate.average_uncertainty_penalty > max_uncertainty:
            candidate.warnings.append(
                f"Failed constraint: max_average_uncertainty ({candidate.average_uncertainty_penalty} > {max_uncertainty})"
            )
            return False

        min_edge = self.config.get("minimum_average_edge", -1.0)
        if candidate.average_edge < min_edge:
            candidate.warnings.append(
                f"Failed constraint: min_average_edge ({candidate.average_edge} < {min_edge})"
            )
            return False

        max_log_loss = self.config.get("maximum_log_loss", float("inf"))
        if metrics.get("log_loss", 0.0) > max_log_loss:
            candidate.warnings.append(
                f"Failed constraint: max_log_loss ({metrics.get('log_loss', 0.0)} > {max_log_loss})"
            )
            return False

        return True
