import uuid
from typing import List, Dict, Any, Optional
from collections import defaultdict
from .contracts import FeedbackSignalAggregateRecord
from ..adjudication.contracts import FeedbackSignalRecord

class FeedbackAggregator:
    @staticmethod
    def aggregate_feedback_signals(signals: List[FeedbackSignalRecord], target_component_family: str, time_span_days: int) -> List[FeedbackSignalAggregateRecord]:
        grouped_signals: Dict[str, List[FeedbackSignalRecord]] = defaultdict(list)
        for s in signals:
            grouped_signals[s.signal_type].append(s)

        aggregates = []
        for signal_type, sig_list in grouped_signals.items():
            if not sig_list:
                continue

            cases = [s.source_resolution_id for s in sig_list]
            common_payload = FeedbackAggregator._extract_common_payload(sig_list)
            contradictions = FeedbackAggregator._count_contradictions(sig_list)

            agg = FeedbackSignalAggregateRecord(
                aggregate_id=str(uuid.uuid4()),
                target_component_family=target_component_family,
                signal_type=signal_type,
                aggregated_cases=cases,
                total_signals=len(sig_list),
                common_payload_elements=common_payload,
                time_span_days=time_span_days,
                contradictory_signals_count=contradictions
            )
            aggregates.append(agg)
        return aggregates

    @staticmethod
    def group_similar_resolutions(signals: List[FeedbackSignalRecord]) -> Dict[str, List[FeedbackSignalRecord]]:
        # Simple grouping by signal type for now
        groups = defaultdict(list)
        for s in signals:
            groups[s.signal_type].append(s)
        return dict(groups)

    @staticmethod
    def _extract_common_payload(signals: List[FeedbackSignalRecord]) -> Dict[str, Any]:
        if not signals:
            return {}
        base_keys = set(signals[0].payload.keys())
        for s in signals[1:]:
            base_keys.intersection_update(s.payload.keys())

        common = {}
        for k in base_keys:
            val = signals[0].payload[k]
            if all(s.payload[k] == val for s in signals):
                common[k] = val
        return common

    @staticmethod
    def _count_contradictions(signals: List[FeedbackSignalRecord]) -> int:
        # A basic contradiction check based on payload content
        # For a real system, this would be more domain-specific
        counts = defaultdict(int)
        for s in signals:
            # Assuming action is the primary deciding factor for contradiction
            action = str(s.payload.get("action", ""))
            counts[action] += 1

        if len(counts) <= 1:
            return 0

        # Count minority actions as contradictions
        max_action_count = max(counts.values())
        total = sum(counts.values())
        return total - max_action_count

    @staticmethod
    def detect_recurrent_case_shapes(aggregates: List[FeedbackSignalAggregateRecord]) -> List[FeedbackSignalAggregateRecord]:
        return [a for a in aggregates if a.total_signals >= 3]

    @staticmethod
    def compute_feedback_consistency(aggregate: FeedbackSignalAggregateRecord) -> float:
        if aggregate.total_signals == 0:
            return 0.0
        return 1.0 - (aggregate.contradictory_signals_count / aggregate.total_signals)
