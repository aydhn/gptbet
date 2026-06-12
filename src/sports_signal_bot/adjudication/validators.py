from typing import List

from .contracts import (
    AdjudicationCaseRecord,
    AdjudicationCaseStatus,
    AdjudicationDecisionRecord,
    KnowledgeScopeRecord,
    KnowledgeScopeType,
)


class AdjudicationGuardrails:
    @staticmethod
    def check_resolution_has_evidence(decision: AdjudicationDecisionRecord) -> bool:
        if not decision.operator_note and not decision.rationale_code:
            return False
        return True

    @staticmethod
    def check_memory_scope_not_overbroad(scope: KnowledgeScopeRecord) -> bool:
        # e.g., disallow global auto-apply
        if (
            scope.scope_type == KnowledgeScopeType.global_advisory_only
            and not scope.constraints.get("auto_apply", False)
        ):
            return True
        if "global" in scope.scope_type.value.lower() and scope.constraints.get(
            "auto_apply", False
        ):
            return False
        return True

    @staticmethod
    def prevent_unresolved_critical_archive(case: AdjudicationCaseRecord) -> bool:
        if (
            case.severity.value == "critical"
            and case.current_status == AdjudicationCaseStatus.unresolved
        ):
            return False
        return True

    @staticmethod
    def validate_secondary_review_bypass(decision: AdjudicationDecisionRecord) -> bool:
        if (
            decision.requires_secondary_review
            and decision.secondary_review_status != "approved"
        ):
            return False
        return True
