from typing import List, Dict, Any
from .contracts import (
    FeedbackSignalAggregateRecord,
    PatternCandidateRecord,
    RuleSuggestionRecordV2,
    SuggestionBundleRecord
)

class LearningDiagnostics:
    @staticmethod
    def print_aggregate_summary(aggregates: List[FeedbackSignalAggregateRecord]) -> None:
        print(f"--- Feedback Aggregates Summary ({len(aggregates)} total) ---")
        for a in aggregates:
            print(f"[{a.target_component_family}] {a.signal_type}: {a.total_signals} signals ({a.contradictory_signals_count} contradictions)")

    @staticmethod
    def print_candidates_summary(candidates: List[PatternCandidateRecord]) -> None:
        print(f"--- Pattern Candidates Summary ({len(candidates)} total) ---")
        for c in candidates:
            print(f"[{c.component_family}] Support: {c.support.strength.value}. Action: {c.candidate_action}")

    @staticmethod
    def print_bundle_summary(bundle: SuggestionBundleRecord) -> None:
        print(f"--- Suggestion Bundle Summary (ID: {bundle.bundle_id}) ---")
        print(f"Aggregate Risk: {bundle.aggregate_risk}")
        for s in bundle.suggestions:
            print(f"  - [{s.suggestion_family.value}] Mode: {s.recommendation_mode.value}. Risk: {s.estimated_risk.risk_level.value}. Confidence: {s.confidence_score.confidence_band.value}")
