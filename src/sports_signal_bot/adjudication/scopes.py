from typing import Any, Dict

from .contracts import KnowledgeScopeRecord, KnowledgeScopeType


class ScopeManager:
    @staticmethod
    def build_knowledge_scope(
        scope_type: KnowledgeScopeType,
        target_value: str,
        constraints: Dict[str, Any] = None,
    ) -> KnowledgeScopeRecord:
        return KnowledgeScopeRecord(
            scope_type=scope_type,
            target_value=target_value,
            constraints=constraints or {},
        )

    @staticmethod
    def validate_scope_safety(scope: KnowledgeScopeRecord) -> bool:
        if scope.scope_type == KnowledgeScopeType.global_advisory_only:
            return True
        if scope.scope_type in [
            KnowledgeScopeType.single_entity,
            KnowledgeScopeType.single_provider_family,
        ]:
            if not scope.target_value:
                return False
        return True

    @staticmethod
    def prevent_overbroad_memory(scope: KnowledgeScopeRecord) -> bool:
        if (
            scope.scope_type == KnowledgeScopeType.sport_specific
            and not scope.target_value
        ):
            return False  # Sport specific needs a sport
        # Simple generic guard
        return True

    @staticmethod
    def explain_scope_restrictions(scope: KnowledgeScopeRecord) -> str:
        return f"Scope is limited to {scope.scope_type.value} with target '{scope.target_value}'."
