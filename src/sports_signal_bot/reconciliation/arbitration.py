from typing import Optional, List, Tuple, Dict, Any
from sports_signal_bot.reconciliation.contracts import (
    ReconciliationGroupRecord, FieldConflictRecord, DisputeRecord,
    TrustedUnifiedRecord
)
from sports_signal_bot.reconciliation.conflicts import detect_conflicts
from sports_signal_bot.reconciliation.confidence import (
    compute_field_confidence, compute_group_confidence
)
from sports_signal_bot.reconciliation.disputes import (
    should_raise_dispute, build_dispute_record
)
from sports_signal_bot.reconciliation.lineage import build_field_lineage
from sports_signal_bot.reconciliation.strategies.balanced_consensus import (
    BalancedConsensusStrategy
)
from sports_signal_bot.reconciliation.strategies.conservative_truth import (
    ConservativeTruthStrategy
)


def _get_strategy(strategy_name: str) -> Any:
    if strategy_name == "conservative_truth":
        return ConservativeTruthStrategy()
    elif strategy_name == "freshness_weighted_odds":
        import sports_signal_bot.reconciliation.strategies as srs
        return srs.freshness_weighted_odds.FreshnessWeightedOddsStrategy()
    elif strategy_name == "stable_source_bias":
        import sports_signal_bot.reconciliation.strategies as srs
        return srs.stable_source_bias.StableSourceBiasStrategy()
    elif strategy_name == "review_heavy_conflict":
        import sports_signal_bot.reconciliation.strategies as srs
        return srs.review_heavy_conflict.ReviewHeavyConflictStrategy()
    return BalancedConsensusStrategy()


def _resolve_fields(
    group: ReconciliationGroupRecord,
    strategy: Any,
    strategy_name: str
) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
    resolved_payload = {}
    field_resolution_map = {}
    lineage_map = {}

    # Collect all fields
    all_fields = set().union(*(obs.payload for obs in group.observations))

    for field in all_fields:
        candidates = {
            obs.provider_name: obs.payload.get(field)
            for obs in group.observations if field in obs.payload
        }
        selected_val = strategy.resolve_field(
            field, candidates, group.observations
        )
        resolved_payload[field] = selected_val
        field_resolution_map[field] = strategy_name
        lineage_map[field] = build_field_lineage(
            field, candidates, selected_val, strategy_name
        ).model_dump()

    return resolved_payload, field_resolution_map, lineage_map


def run_arbitration(
    group: ReconciliationGroupRecord,
    strategy_name: str = "balanced_consensus"
) -> Tuple[
    Optional[TrustedUnifiedRecord],
    List[FieldConflictRecord],
    Optional[DisputeRecord]
]:
    conflicts = detect_conflicts(group)

    if should_raise_dispute(conflicts):
        dispute = build_dispute_record(group, conflicts)
        return None, conflicts, dispute

    strategy = _get_strategy(strategy_name)

    resolved_payload, field_resolution_map, lineage_map = _resolve_fields(
        group, strategy, strategy_name
    )

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
