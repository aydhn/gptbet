from typing import Optional

from typing import List, Tuple, Dict, Any
from sports_signal_bot.reconciliation.contracts import (
    ReconciliationGroupRecord, FieldConflictRecord, DisputeRecord,
    TrustedUnifiedRecord, ConsensusLineageRecord
)
from sports_signal_bot.reconciliation.conflicts import detect_conflicts
from sports_signal_bot.reconciliation.confidence import compute_field_confidence, compute_group_confidence, classify_confidence_band
from sports_signal_bot.reconciliation.disputes import should_raise_dispute, build_dispute_record
from sports_signal_bot.reconciliation.lineage import build_field_lineage
from sports_signal_bot.reconciliation.strategies.balanced_consensus import BalancedConsensusStrategy
from sports_signal_bot.reconciliation.strategies.conservative_truth import ConservativeTruthStrategy

def run_arbitration(group: ReconciliationGroupRecord, strategy_name: str = "balanced_consensus") -> Tuple[Optional[TrustedUnifiedRecord], List[FieldConflictRecord], Optional[DisputeRecord]]:
    conflicts = detect_conflicts(group)

    if should_raise_dispute(conflicts):
        dispute = build_dispute_record(group, conflicts)
        return None, conflicts, dispute


    strategy = BalancedConsensusStrategy()
    if strategy_name == "conservative_truth":
        strategy = ConservativeTruthStrategy()
    elif strategy_name == "freshness_weighted_odds":
        from sports_signal_bot.reconciliation.strategies.freshness_weighted_odds import FreshnessWeightedOddsStrategy
        strategy = FreshnessWeightedOddsStrategy()
    elif strategy_name == "stable_source_bias":
        from sports_signal_bot.reconciliation.strategies.stable_source_bias import StableSourceBiasStrategy
        strategy = StableSourceBiasStrategy()
    elif strategy_name == "review_heavy_conflict":
        from sports_signal_bot.reconciliation.strategies.review_heavy_conflict import ReviewHeavyConflictStrategy
        strategy = ReviewHeavyConflictStrategy()


    resolved_payload = {}
    field_resolution_map = {}
    lineage_map = {}

    # Collect all fields
    all_fields = set()
    for obs in group.observations:
        all_fields.update(obs.payload.keys())

    for field in all_fields:
        candidates = {obs.provider_name: obs.payload.get(field) for obs in group.observations if field in obs.payload}
        selected_val = strategy.resolve_field(field, candidates, group.observations)
        resolved_payload[field] = selected_val
        field_resolution_map[field] = strategy_name
        lineage_map[field] = build_field_lineage(field, candidates, selected_val, strategy_name).model_dump()

    field_conf = compute_field_confidence(conflicts)
    conf_score = compute_group_confidence([field_conf])

    unified = TrustedUnifiedRecord(
        entity_key=group.entity_key,
        data_family=group.data_family,
        trusted_payload=resolved_payload,
        field_resolution_map=field_resolution_map,
        selected_source_refs=group.providers_involved,
        consensus_strategy=strategy_name,
        confidence_score=conf_score,
        dispute_flags=[],
        lineage=lineage_map,
        warnings=[]
    )

    return unified, conflicts, None
