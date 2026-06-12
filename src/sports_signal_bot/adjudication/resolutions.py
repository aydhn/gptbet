import uuid
from typing import Any, Dict

from .contracts import (HumanCorrectionInput, HumanCorrectionRecord,
                        ResolutionInput, ResolutionRecord)


class ResolutionApplier:
    @staticmethod
    def create_resolution(
        input_data: ResolutionInput,
    ) -> ResolutionRecord:

        # Categorize families for simplistic reporting
        family = "unknown"
        if (
            "accept" in input_data.resolution_type.value
            or "override" in input_data.resolution_type.value
            or "alias" in input_data.resolution_type.value
            or "identity" in input_data.resolution_type.value
            or "consensus" in input_data.resolution_type.value
            or "split" in input_data.resolution_type.value
        ):
            family = "data_entity"
        elif (
            "policy" in input_data.resolution_type.value
            or "block" in input_data.resolution_type.value
            or "no_bet" in input_data.resolution_type.value
            or "borderline" in input_data.resolution_type.value
        ):
            family = "decision_policy"
        elif (
            "precedent" in input_data.resolution_type.value
            or "rule" in input_data.resolution_type.value
            or "memory" in input_data.resolution_type.value
        ):
            family = "knowledge_memory"
        elif "provider" in input_data.resolution_type.value:
            family = "provider_trust"

        return ResolutionRecord(
            resolution_id=str(uuid.uuid4()),
            case_id=input_data.case_id,
            resolution_family=family,
            resolution_status="applied",
            corrected_value=input_data.corrected_value,
            chosen_source=input_data.chosen_source,
            selected_precedent=input_data.selected_precedent,
            feedback_eligibility=input_data.feedback_eligibility,
            memory_write_allowed=input_data.memory_write_allowed,
            effective_scope=input_data.effective_scope,
            related_entities=[],
            caveats=input_data.caveats or [],
        )


class HumanCorrectionBuilder:
    @staticmethod
    def build_human_correction(
        request: HumanCorrectionInput,
    ) -> HumanCorrectionRecord:
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
