from typing import List, Dict, Any
from .contracts import (
    SuggestionScopeRecord,
    SuggestionScopeType,
    RuleExtractionRecord
)

class ScopeManager:
    @staticmethod
    def build_suggestion_scope(extraction: RuleExtractionRecord) -> SuggestionScopeRecord:
        # Infer scope based on conditions
        scope_type = SuggestionScopeType.provider_and_family_scoped
        target_entities = []

        if "provider_id" in extraction.condition_block:
            target_entities.append(extraction.condition_block["provider_id"])
        if "entity_a" in extraction.condition_block:
            target_entities.extend([extraction.condition_block["entity_a"], extraction.condition_block.get("entity_b", "")])
            scope_type = SuggestionScopeType.single_entity

        blast_radius = ScopeManager.compute_scope_blast_radius(scope_type, target_entities)
        is_safe = ScopeManager.validate_scope_safety(scope_type, blast_radius)

        return SuggestionScopeRecord(
            scope_type=scope_type,
            target_entities=target_entities,
            constraints={"requires_stable_ops": True},
            is_safe=is_safe,
            blast_radius_estimate=blast_radius
        )

    @staticmethod
    def compute_scope_blast_radius(scope_type: SuggestionScopeType, target_entities: List[str]) -> str:
        if scope_type == SuggestionScopeType.single_entity:
            return "narrow"
        elif scope_type == SuggestionScopeType.provider_and_family_scoped:
            return "medium"
        elif scope_type in [SuggestionScopeType.sport_specific, SuggestionScopeType.market_specific]:
            return "wide"
        return "global"

    @staticmethod
    def validate_scope_safety(scope_type: SuggestionScopeType, blast_radius: str) -> bool:
        if scope_type == SuggestionScopeType.prohibited_global_change:
            return False
        if blast_radius == "global":
            return False
        return True

    @staticmethod
    def narrow_scope_if_needed(scope: SuggestionScopeRecord) -> SuggestionScopeRecord:
        if not scope.is_safe:
            # Force to a safer scope level
            if scope.scope_type == SuggestionScopeType.prohibited_global_change:
                scope.scope_type = SuggestionScopeType.advisory_global
            scope.blast_radius_estimate = "narrowed"
            scope.is_safe = True
            scope.constraints["narrowed_from_unsafe"] = True
        return scope

    @staticmethod
    def explain_scope_limitations(scope: SuggestionScopeRecord) -> str:
        return f"Scope is {scope.scope_type.value} with {scope.blast_radius_estimate} impact. Targets: {scope.target_entities}"
