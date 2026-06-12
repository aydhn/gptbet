from typing import Any, Dict, List, Optional

from .contracts import AdjudicationCaseRecord, AdjudicationDecisionRecord


class EvidenceIntegrator:
    @staticmethod
    def attach_evidence_to_case(
        case: AdjudicationCaseRecord, evidence_bundle_ref: str
    ) -> None:
        case.evidence_bundle_ref = evidence_bundle_ref

    @staticmethod
    def validate_resolution_against_evidence(
        decision: AdjudicationDecisionRecord, evidence_data: Dict[str, Any]
    ) -> bool:
        # In a real system, verify the operator cited evidence that actually exists in the bundle
        # For this skeleton, just ensure an operator note or rationale was provided
        if not decision.operator_note and not decision.rationale_code:
            decision.warnings.append(
                "Resolution lacks explicit rationale or note linking to evidence."
            )
            return False
        return True

    @staticmethod
    def summarize_supporting_evidence(
        decision: AdjudicationDecisionRecord, evidence_data: Dict[str, Any]
    ) -> str:
        # Dummy summary generator
        return f"Operator {decision.operator_id} provided rationale '{decision.rationale_code}' based on evidence bundle."

    @staticmethod
    def mark_resolution_caveats(
        decision: AdjudicationDecisionRecord, evidence_data: Dict[str, Any]
    ) -> List[str]:
        caveats = []
        if decision.confidence_in_resolution < 0.8:
            caveats.append("Low confidence resolution.")
        if (
            "conflict" in decision.resolution_type.value.lower()
            and decision.requires_secondary_review
        ):
            caveats.append("Pending secondary review for conflict resolution.")
        return caveats
