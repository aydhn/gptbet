import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    RuleSuggestionRecordV2,
    AssimilationDecisionRecord,
    SuggestionStatus,
    SuggestionSimulationRecord
)
from .simulation import SimulationManager

class AssimilationEngine:
    @staticmethod
    def build_assimilation_decision(suggestion: RuleSuggestionRecordV2) -> AssimilationDecisionRecord:
        status = SuggestionStatus.generated
        review_route = AssimilationEngine.assign_review_route(suggestion)
        sim_required = AssimilationEngine.determine_simulation_requirement(suggestion)
        release_path = SimulationManager.determine_release_path_for_suggestion(suggestion)

        rationale = f"Assimilated with mode {suggestion.recommendation_mode.value}. "

        if suggestion.recommendation_mode == "blocked":
            status = SuggestionStatus.rejected
            rationale += "Suggestion was blocked due to safety/confidence checks."
        elif suggestion.recommendation_mode == "advisory_only":
            status = SuggestionStatus.advisory_only
            rationale += "Kept as advisory per confidence/risk profile."
        elif suggestion.recommendation_mode == "manual_review_required":
            status = SuggestionStatus.pending_review
            rationale += "Routed for manual review due to risk/impact."
        elif suggestion.recommendation_mode == "candidate_patch":
            status = SuggestionStatus.promoted_to_candidate_patch
            rationale += "Promoted to candidate patch. Good support and safe scope."

        return AssimilationDecisionRecord(
            decision_id=str(uuid.uuid4()),
            suggestion_id=suggestion.suggestion_id,
            decision_status=status,
            assigned_review_route=review_route,
            simulation_required=sim_required,
            release_path_proposed=release_path,
            rationale=rationale
        )

    @staticmethod
    def assign_review_route(suggestion: RuleSuggestionRecordV2) -> str:
        if suggestion.recommendation_mode == "manual_review_required":
            if suggestion.estimated_risk.risk_level == "critical":
                return "principal_engineer_review"
            return "operator_review"
        return "none"

    @staticmethod
    def determine_simulation_requirement(suggestion: RuleSuggestionRecordV2) -> bool:
        return suggestion.recommendation_mode in ["candidate_patch", "candidate_rule_bundle", "manual_review_required"]

    @staticmethod
    def summarize_assimilation_outcome(decision: AssimilationDecisionRecord) -> str:
        return f"Status: {decision.decision_status.value}. Route: {decision.assigned_review_route}. Sim Required: {decision.simulation_required}"
