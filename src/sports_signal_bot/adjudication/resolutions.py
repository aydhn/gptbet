import uuid
from typing import Any, Dict, List, Optional

from .contracts import (HumanCorrectionInput, HumanCorrectionRecord,
                        ResolutionRecord, ResolutionType)


class ResolutionApplier:
    @staticmethod
    def create_resolution(
        case_id: str,
        resolution_type: ResolutionType,
        feedback_eligibility: bool,
        memory_write_allowed: bool,
        effective_scope: str,
        corrected_value: Optional[Any] = None,
        chosen_source: Optional[str] = None,
        selected_precedent: Optional[str] = None,
        caveats: Optional[List[str]] = None,
    ) -> ResolutionRecord:

        # Categorize families for simplistic reporting
        family = "unknown"
        if (
            "accept" in resolution_type.value
            or "override" in resolution_type.value
            or "alias" in resolution_type.value
            or "identity" in resolution_type.value
            or "consensus" in resolution_type.value
            or "split" in resolution_type.value
        ):
            family = "data_entity"
        elif (
            "policy" in resolution_type.value
            or "block" in resolution_type.value
            or "no_bet" in resolution_type.value
            or "borderline" in resolution_type.value
        ):
            family = "decision_policy"
        elif (
            "precedent" in resolution_type.value
            or "rule" in resolution_type.value
            or "memory" in resolution_type.value
        ):
            family = "knowledge_memory"
        elif "provider" in resolution_type.value:
            family = "provider_trust"

        return ResolutionRecord(
            resolution_id=str(uuid.uuid4()),
            case_id=case_id,
            resolution_family=family,
            resolution_status="applied",
            corrected_value=corrected_value,
            chosen_source=chosen_source,
            selected_precedent=selected_precedent,
            feedback_eligibility=feedback_eligibility,
            memory_write_allowed=memory_write_allowed,
            effective_scope=effective_scope,
            related_entities=[],
            caveats=caveats or [],
        )


class HumanCorrectionBuilder:
    @staticmethod
    def build_human_correction(request: HumanCorrectionInput) -> HumanCorrectionRecord:
        return HumanCorrectionRecord(
            correction_id=str(uuid.uuid4()),
            case_id=request.case_id,
            corrected_field=request.corrected_field,
            old_value=request.old_value,
            new_value=request.new_value,
            resolution_basis=request.resolution_basis,
            evidence_refs=request.evidence_refs or [],
            scope=request.scope,
            confidence=request.confidence,
            reversibility=request.reversibility,
            propagate_to_memory=request.propagate_to_memory,
        )

    @staticmethod
    def validate_correction_payload(correction: HumanCorrectionRecord) -> bool:
        if correction.confidence < 0.0 or correction.confidence > 1.0:
            return False
        if correction.propagate_to_memory and not correction.evidence_refs:
            # Simple rule: if we propagate, we want evidence
            return False
        return True

    @staticmethod
    def compare_before_after_resolution(
        correction: HumanCorrectionRecord,
    ) -> Dict[str, Any]:
        return {
            "field": correction.corrected_field,
            "old": correction.old_value,
            "new": correction.new_value,
            "changed": correction.old_value != correction.new_value,
        }

    @staticmethod
    def classify_correction_risk(correction: HumanCorrectionRecord) -> str:
        if (
            correction.propagate_to_memory
            and correction.scope == "global_advisory_only"
        ):
            return "low"
        if not correction.reversibility:
            return "high"
        if correction.confidence < 0.7:
            return "medium"
        return "low"
