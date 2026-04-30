from typing import List, Dict, Any
from .contracts import (
    SuggestionRiskRecord,
    SuggestionRiskLevel,
    SuggestionScopeRecord
)

class RiskClassifier:
    @staticmethod
    def classify_suggestion_risk(scope: SuggestionScopeRecord, target_component: str, action_type: str) -> SuggestionRiskRecord:
        drivers = []
        risk_level = SuggestionRiskLevel.low

        # Scope-based risk
        if scope.blast_radius_estimate == "wide":
            drivers.append("wide_blast_radius")
            risk_level = SuggestionRiskLevel.high
        elif scope.blast_radius_estimate == "global":
            drivers.append("global_blast_radius")
            risk_level = SuggestionRiskLevel.critical

        # Action-based risk
        overrides_boundary = False
        if action_type in ["adjust_threshold", "shift_boundary"]:
            drivers.append("boundary_modification")
            overrides_boundary = True
            if risk_level == SuggestionRiskLevel.low:
                risk_level = SuggestionRiskLevel.medium

        # Component-based risk
        critical_components = ["policy", "threshold", "release"]
        if any(c in target_component for c in critical_components):
            drivers.append("critical_component_target")
            if risk_level in [SuggestionRiskLevel.low, SuggestionRiskLevel.medium]:
                risk_level = SuggestionRiskLevel.high

        return SuggestionRiskRecord(
            risk_level=risk_level,
            scope_breadth=scope.blast_radius_estimate,
            target_component_criticality="high" if "critical_component_target" in drivers else "medium",
            historical_instability=False, # Would need historical data
            overrides_safety_boundary=overrides_boundary,
            downstream_blast_radius=scope.blast_radius_estimate,
            risk_drivers=drivers
        )

    @staticmethod
    def detect_safety_boundary_change(action_block: Dict[str, Any]) -> bool:
        return action_block.get("type") in ["shift_boundary", "relax_threshold", "override_policy"]

    @staticmethod
    def summarize_risk_drivers(risk: SuggestionRiskRecord) -> str:
        return f"Risk Level: {risk.risk_level.value}. Drivers: {', '.join(risk.risk_drivers)}"
