from typing import List, Dict
from .contracts import StandardizedPredictionRecord, EnsembleInputRecord

def group_predictions_by_event_market(predictions: List[StandardizedPredictionRecord]) -> List[EnsembleInputRecord]:
    """Groups a flat list of predictions into EnsembleInputRecords."""
    grouped: Dict[str, List[StandardizedPredictionRecord]] = {}

    for p in predictions:
        key = f"{p.event_id}_{p.sport}_{p.market_type}"
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(p)

    records = []
    for key, preds in grouped.items():
        if not preds:
            continue
        first = preds[0]
        records.append(
            EnsembleInputRecord(
                event_id=first.event_id,
                sport=first.sport,
                market_type=first.market_type,
                predictions=preds
            )
        )

    return records
