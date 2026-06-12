import uuid
from typing import Any, Dict, List, Optional

from .contracts import (
    FeedbackApplicationRecord,
    FeedbackSignalRecord,
    FeedbackStatus,
    PolicyFeedbackRecord,
    ResolutionRecord,
    RuleSuggestionBundleRecord,
    RuleSuggestionRecord,
    ThresholdFeedbackRecord,
)


class FeedbackIngestor:
    @staticmethod
    def derive_feedback_signal(
        resolution: ResolutionRecord,
        payload: Dict[str, Any],
        confidence: float,
        signal_type: str = "generic",
    ) -> Optional[FeedbackSignalRecord]:
        if not resolution.feedback_eligibility:
            return None

        return FeedbackSignalRecord(
            signal_id=str(uuid.uuid4()),
            source_resolution_id=resolution.resolution_id,
            signal_type=signal_type,
            payload=payload,
            status=FeedbackStatus.captured,
            confidence=confidence,
        )

    @staticmethod
    def validate_feedback_for_memory(signal: FeedbackSignalRecord) -> bool:
        if signal.confidence < 0.6:
            return False
        if "sensitive" in signal.payload.get("tags", []):
            return False
        return True

    @staticmethod
    def classify_feedback_strength(signal: FeedbackSignalRecord) -> str:
        if signal.confidence >= 0.9:
            return "strong"
        elif signal.confidence >= 0.7:
            return "moderate"
        else:
            return "weak"

    @staticmethod
    def publish_feedback_application(
        feedback_id: str,
        auto_apply: bool,
        requires_secondary_review: bool,
        scope_limit: str,
        risk_level: str,
    ) -> FeedbackApplicationRecord:
        return FeedbackApplicationRecord(
            application_id=str(uuid.uuid4()),
            feedback_id=feedback_id,
            auto_apply_allowed=auto_apply,
            requires_secondary_review=requires_secondary_review,
            scope_limit=scope_limit,
            risk_level=risk_level,
            consumer_components=["memory_store", "reconciliation_engine"],
        )

    @staticmethod
    def summarize_feedback_outcomes(
        signals: List[FeedbackSignalRecord],
    ) -> Dict[str, int]:
        summary = {"captured": 0, "accepted_for_memory": 0, "rejected": 0}
        for s in signals:
            if s.status == FeedbackStatus.captured:
                summary["captured"] += 1
            elif s.status == FeedbackStatus.accepted_for_memory:
                summary["accepted_for_memory"] += 1
            elif s.status == FeedbackStatus.rejected_for_memory:
                summary["rejected"] += 1
        return summary


class FeedbackLoopIntegrator:
    @staticmethod
    def convert_resolution_to_reconciliation_feedback(
        resolution: ResolutionRecord,
    ) -> Dict[str, Any]:
        return {
            "resolution_id": resolution.resolution_id,
            "chosen_source": resolution.chosen_source,
            "corrected_value": resolution.corrected_value,
            "action": "reconciliation_update",
        }

    @staticmethod
    def build_provider_pattern_memory(
        resolution: ResolutionRecord, provider_id: str, conflict_pattern: str
    ) -> Dict[str, Any]:
        return {
            "provider_id": provider_id,
            "pattern": conflict_pattern,
            "recommendation": (
                "decrease_trust"
                if resolution.resolution_family == "provider_trust"
                else "monitor"
            ),
        }

    @staticmethod
    def build_alias_resolution_memory(
        resolution: ResolutionRecord, entity_a: str, entity_b: str, mapped_id: str
    ) -> Dict[str, Any]:
        return {
            "entity_a": entity_a,
            "entity_b": entity_b,
            "resolved_identity": mapped_id,
        }

    @staticmethod
    def build_result_resolution_advisory(
        resolution: ResolutionRecord, event_id: str, final_score: str
    ) -> Dict[str, Any]:
        return {
            "event_id": event_id,
            "final_score": final_score,
            "advisory_note": "Human reviewed settlement",
        }

    @staticmethod
    def derive_policy_feedback(
        case_id: str, policy_ref: str, note: str
    ) -> PolicyFeedbackRecord:
        return PolicyFeedbackRecord(
            feedback_id=str(uuid.uuid4()),
            case_id=case_id,
            policy_ref=policy_ref,
            feedback_note=note,
        )

    @staticmethod
    def derive_threshold_feedback(
        case_id: str, threshold_ref: str, suggested_value: float, rationale: str
    ) -> ThresholdFeedbackRecord:
        return ThresholdFeedbackRecord(
            feedback_id=str(uuid.uuid4()),
            case_id=case_id,
            threshold_ref=threshold_ref,
            suggested_value=suggested_value,
            rationale=rationale,
        )

    @staticmethod
    def build_rule_suggestion_bundle(
        suggestions: List[RuleSuggestionRecord],
    ) -> RuleSuggestionBundleRecord:
        return RuleSuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()), suggestions=suggestions
        )

    @staticmethod
    def keep_feedback_nonbinding_by_default(
        app_record: FeedbackApplicationRecord,
    ) -> None:
        if app_record.risk_level in ["high", "critical"]:
            app_record.auto_apply_allowed = False
            app_record.requires_secondary_review = True

    @staticmethod
    def derive_provider_feedback_from_resolution(
        resolution: ResolutionRecord, provider_id: str
    ) -> Dict[str, Any]:
        return {
            "provider_id": provider_id,
            "penalized": "penalize" in str(resolution.resolution_family).lower(),
        }

    @staticmethod
    def apply_human_confirmed_reputation_adjustment(
        provider_id: str, adjustment: float
    ) -> Dict[str, Any]:
        return {"provider_id": provider_id, "reputation_adjustment": adjustment}

    @staticmethod
    def prevent_small_sample_overreaction(case_count: int, threshold: int = 5) -> bool:
        return case_count < threshold

    @staticmethod
    def summarize_provider_feedback_effect(
        provider_id: str, adjustments: List[float]
    ) -> str:
        total = sum(adjustments)
        return f"Provider {provider_id} net adjustment: {total}"
