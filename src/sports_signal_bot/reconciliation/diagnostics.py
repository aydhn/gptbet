
from sports_signal_bot.reconciliation.contracts import ReconciliationSummaryRecord

def summarize_reconciliation(groups, conflicts, disputes) -> ReconciliationSummaryRecord:
    conf_dist = {"high_confidence": 0, "medium_confidence": 0, "low_confidence": 0, "disputed": 0, "unresolved": 0}
    for g in groups:
        if g.confidence_score >= 0.8:
            conf_dist["high_confidence"] += 1
        elif g.confidence_score >= 0.5:
            conf_dist["medium_confidence"] += 1
        else:
            conf_dist["low_confidence"] += 1

    auto_resolved = len(groups) - len(disputes)
    ratio = auto_resolved / len(groups) if groups else 0.0

    return ReconciliationSummaryRecord(
        reconciled_group_count=len(groups),
        conflict_count=len(conflicts),
        dispute_count=len(disputes),
        confidence_distribution=conf_dist,
        provider_disagreement_burden={},
        auto_resolved_ratio=ratio
    )
