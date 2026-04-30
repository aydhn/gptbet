import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    RuleSuggestionRecordV2,
    SuggestionSimulationRecord
)

class SimulationManager:
    @staticmethod
    def estimate_suggestion_impact(suggestion: RuleSuggestionRecordV2) -> int:
        # Placeholder for estimating how many runs/markets would be affected
        # In a real system, this would query historical data
        if suggestion.scope.blast_radius_estimate == "narrow":
            return 10
        elif suggestion.scope.blast_radius_estimate == "medium":
            return 100
        elif suggestion.scope.blast_radius_estimate == "wide":
            return 1000
        return 10000

    @staticmethod
    def build_sandbox_evaluation_plan(suggestion: RuleSuggestionRecordV2) -> SuggestionSimulationRecord:
        impact = SimulationManager.estimate_suggestion_impact(suggestion)

        required_gates = []
        if suggestion.estimated_risk.risk_level in ["high", "critical"]:
            required_gates.extend(["full_regression_suite", "financial_impact_smoke_test"])
        else:
            required_gates.append("basic_smoke_test")

        if suggestion.target_component_family in ["threshold", "policy"]:
            required_gates.append("threshold_boundary_regression")

        return SuggestionSimulationRecord(
            simulation_id=str(uuid.uuid4()),
            suggestion_id=suggestion.suggestion_id,
            affected_runs_estimate=impact,
            dry_run_supported=True,
            required_quality_gates=required_gates,
            approval_required=suggestion.recommendation_mode == "manual_review_required"
        )

    @staticmethod
    def list_required_quality_gates(simulation_plan: SuggestionSimulationRecord) -> List[str]:
        return simulation_plan.required_quality_gates

    @staticmethod
    def determine_release_path_for_suggestion(suggestion: RuleSuggestionRecordV2) -> str:
        if suggestion.recommendation_mode == "candidate_patch":
            return "candidate_release_channel"
        elif suggestion.recommendation_mode == "manual_review_required":
            return "approval_queue"
        return "advisory_backlog"
