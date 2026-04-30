
from typing import List, Any, Dict
from sports_signal_bot.reconciliation.contracts import ConsensusLineageRecord

def build_field_lineage(field_name: str, candidates: Dict[str, Any], selected_val: Any, strategy: str) -> ConsensusLineageRecord:
    return ConsensusLineageRecord(
        field_name=field_name,
        candidate_sources=list(candidates.keys()),
        candidate_values=list(candidates.values()),
        selected_value=selected_val,
        strategy_used=strategy,
        trust_scores={},
        decision_explanation=f"Resolved via {strategy}"
    )

def attach_consensus_lineage(record: Any, lineage: ConsensusLineageRecord) -> None:
    pass

def summarize_resolution_path(lineage: ConsensusLineageRecord) -> str:
    return f"{lineage.field_name} resolved to {lineage.selected_value} via {lineage.strategy_used}"

def export_lineage_trace(lineage: ConsensusLineageRecord) -> Dict[str, Any]:
    return lineage.model_dump()
