import uuid
from typing import List, Dict, Any, Optional
from .contracts import (
    FeedbackSignalAggregateRecord,
    PatternCandidateRecord,
    PatternSupportRecord,
    SupportStrength,
    PatternConflictRecord
)

class PatternMiner:
    @staticmethod
    def fingerprint_pattern(aggregate: FeedbackSignalAggregateRecord) -> str:
        # Create a unique signature for the pattern
        keys = sorted(aggregate.common_payload_elements.keys())
        sig_parts = [f"{k}:{aggregate.common_payload_elements[k]}" for k in keys]
        return f"{aggregate.signal_type}|{','.join(sig_parts)}"

    @staticmethod
    def compute_support_strength(support_count: int, unique_cases: int, contradiction_burden: float) -> SupportStrength:
        if support_count < 3 or unique_cases < 2:
            return SupportStrength.insufficient
        if contradiction_burden > 0.3:
            return SupportStrength.weak
        if support_count >= 10 and unique_cases >= 5 and contradiction_burden < 0.1:
            return SupportStrength.strong
        return SupportStrength.moderate

    @staticmethod
    def compute_evidence_diversity(aggregate: FeedbackSignalAggregateRecord) -> float:
        # Simplified diversity metric based on ratio of unique cases to total signals
        if aggregate.total_signals == 0:
            return 0.0
        return len(aggregate.aggregated_cases) / aggregate.total_signals

    @staticmethod
    def compute_contradiction_burden(aggregate: FeedbackSignalAggregateRecord) -> float:
        if aggregate.total_signals == 0:
            return 0.0
        return aggregate.contradictory_signals_count / aggregate.total_signals

    @staticmethod
    def compute_recency_weight(time_span_days: int) -> float:
        # Exponential decay-like function for recency
        if time_span_days <= 7:
            return 1.0
        elif time_span_days <= 30:
            return 0.8
        elif time_span_days <= 90:
            return 0.5
        return 0.2

    @staticmethod
    def explain_support_profile(support: PatternSupportRecord) -> str:
        return f"Support: {support.strength.value} ({support.support_count} signals, {support.distinct_case_count} unique cases, {support.contradiction_burden:.2f} contradiction)"

    @staticmethod
    def build_pattern_candidate(aggregate: FeedbackSignalAggregateRecord) -> PatternCandidateRecord:
        diversity = PatternMiner.compute_evidence_diversity(aggregate)
        burden = PatternMiner.compute_contradiction_burden(aggregate)
        recency = PatternMiner.compute_recency_weight(aggregate.time_span_days)

        strength = PatternMiner.compute_support_strength(aggregate.total_signals, len(aggregate.aggregated_cases), burden)

        support = PatternSupportRecord(
            support_count=aggregate.total_signals,
            distinct_case_count=len(aggregate.aggregated_cases),
            distinct_operator_count=1, # Defaulting to 1 for now, would need operator tracking
            distinct_period_count=max(1, aggregate.time_span_days // 7),
            evidence_diversity_score=diversity,
            contradiction_burden=burden,
            recency_weight=recency,
            precedent_alignment=1.0, # Defaulting, would need precedent checking
            strength=strength
        )

        # Simplified action extraction
        action = str(aggregate.common_payload_elements.get("action", "unknown_action"))

        return PatternCandidateRecord(
            pattern_id=str(uuid.uuid4()),
            pattern_signature=PatternMiner.fingerprint_pattern(aggregate),
            component_family=aggregate.target_component_family,
            condition_summary=aggregate.common_payload_elements,
            support=support,
            unique_case_count=len(aggregate.aggregated_cases),
            operator_consistency=1.0 - burden,
            time_span=f"{aggregate.time_span_days} days",
            scope="narrow", # Default scope
            contradictory_cases=[], # Not tracked at case level yet
            candidate_action=action
        )

    @staticmethod
    def detect_pattern_contradictions(candidates: List[PatternCandidateRecord]) -> List[PatternConflictRecord]:
        conflicts = []
        for i, c1 in enumerate(candidates):
            for c2 in candidates[i+1:]:
                # Check for same signature but different actions
                if c1.condition_summary == c2.condition_summary and c1.candidate_action != c2.candidate_action:
                    conflicts.append(PatternConflictRecord(
                        conflict_id=str(uuid.uuid4()),
                        pattern_a_id=c1.pattern_id,
                        pattern_b_id=c2.pattern_id,
                        conflict_description=f"Action mismatch for similar conditions: {c1.candidate_action} vs {c2.candidate_action}"
                    ))
        return conflicts

    @staticmethod
    def compute_pattern_reliability(candidate: PatternCandidateRecord) -> float:
        if candidate.support.strength == SupportStrength.insufficient:
            return 0.0

        base_score = 0.5
        if candidate.support.strength == SupportStrength.strong:
            base_score = 0.9
        elif candidate.support.strength == SupportStrength.moderate:
            base_score = 0.7

        # Penalize for contradiction burden
        return max(0.0, base_score - (candidate.support.contradiction_burden * 0.5))

    @staticmethod
    def suppress_spurious_patterns(candidates: List[PatternCandidateRecord]) -> List[PatternCandidateRecord]:
        return [c for c in candidates if c.support.strength != SupportStrength.insufficient]
