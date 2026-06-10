from typing import List, Dict, Any
from collections import defaultdict
from sports_signal_bot.reconciliation.contracts import (
    SourceObservationRecord,
    ReconciliationGroupRecord,
)


def build_reconciliation_groups(
    observations: List[SourceObservationRecord],
) -> List[ReconciliationGroupRecord]:
    groups_map = defaultdict(list)
    for obs in observations:
        key = obs.entity_key
        groups_map[key].append(obs)

    return [
        ReconciliationGroupRecord(
            group_id=f"group_{key}",
            data_family=obs_list[0].data_family,
            sport=obs_list[0].sport,
            entity_key=key,
            source_count=len(obs_list),
            providers_involved=list({o.provider_name for o in obs_list}),
            reconciliation_status="pending",
            conflict_count=0,
            confidence_score=0.0,
            selected_consensus_strategy="none",
            observations=obs_list,
        )
        for key, obs_list in groups_map.items()
    ]


def resolve_grouping_identity(group: ReconciliationGroupRecord) -> bool:
    return True


def detect_grouping_ambiguity(group: ReconciliationGroupRecord) -> List[str]:
    return []


def merge_observations_by_entity(
    observations: List[SourceObservationRecord],
) -> Dict[str, List[SourceObservationRecord]]:
    pass


def summarize_grouping_quality(
    groups: List[ReconciliationGroupRecord],
) -> Dict[str, Any]:
    return {"total_groups": len(groups)}
