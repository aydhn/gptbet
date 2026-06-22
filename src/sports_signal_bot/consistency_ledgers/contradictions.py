from typing import Any, Dict, List, Tuple

from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyContradictionRecord,
    ConsistencyLedgerEntryRecord,
    ConsistencyState,
    ContradictionFamily,
    SovereignGovernanceConsistencyLedgerRecord,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def detect_consistency_contradictions(
    ledger: SovereignGovernanceConsistencyLedgerRecord,
    entries: Dict[str, ConsistencyLedgerEntryRecord],
) -> List[ConsistencyContradictionRecord]:
    contradictions = []

    # Simple mock logic: Look for entries with conflicting caveats or freshness issues
    freshness_issues = []
    no_safe_issues = []

    for entry_id in ledger.entry_refs:
        if entry_id not in entries:
            continue
        entry = entries[entry_id]
        if entry.currentness_state != "current":
            freshness_issues.append(entry_id)
        if "no_safe" in entry.caveat_state:
            no_safe_issues.append(entry_id)

    if len(freshness_issues) >= 2:
        contradictions.append(
            ConsistencyContradictionRecord(
                contradiction_id=generate_id("contra"),
                ledger_id=ledger.consistency_ledger_id,
                contradiction_family=ContradictionFamily.FRESHNESS_CONTRADICTION,
                involved_entry_refs=freshness_issues,
                severity="high",
                warnings=["Multiple stale entries detected forming a contradiction."],
            )
        )

    if no_safe_issues:
        contradictions.append(
            ConsistencyContradictionRecord(
                contradiction_id=generate_id("contra"),
                ledger_id=ledger.consistency_ledger_id,
                contradiction_family=ContradictionFamily.NO_SAFE_VISIBILITY_CONTRADICTION,
                involved_entry_refs=no_safe_issues,
                severity="critical",
                warnings=[
                    "No-safe visibility contradiction detected. Must be preserved."
                ],
            )
        )

    for c in contradictions:
        ledger.contradiction_refs.append(c.contradiction_id)

    return contradictions


def classify_contradiction_severity(
    contradiction: ConsistencyContradictionRecord,
) -> str:
    if contradiction.contradiction_family in [
        ContradictionFamily.NO_SAFE_VISIBILITY_CONTRADICTION,
        ContradictionFamily.SOVEREIGNTY_VISIBILITY_CONTRADICTION,
    ]:
        return "critical"
    if contradiction.contradiction_family in [
        ContradictionFamily.FRESHNESS_CONTRADICTION,
        ContradictionFamily.TRACE_CONTRADICTION,
    ]:
        return "high"
    return "moderate"


def explain_contradiction_lineage(
    contradiction: ConsistencyContradictionRecord,
    entries: Dict[str, ConsistencyLedgerEntryRecord],
) -> Dict[str, Any]:
    details = []
    for e_ref in contradiction.involved_entry_refs:
        if e_ref in entries:
            e = entries[e_ref]
            details.append(
                f"Entry {e.consistency_entry_id} from {e.source_family} (Currentness: {e.currentness_state}, Caveats: {e.caveat_state})"
            )
    return {
        "contradiction_id": contradiction.contradiction_id,
        "family": contradiction.contradiction_family.value,
        "severity": contradiction.severity,
        "involved_entries": details,
    }


def summarize_contradiction_burden(
    contradictions: List[ConsistencyContradictionRecord],
) -> Dict[str, Any]:
    critical = sum(1 for c in contradictions if c.severity == "critical")
    high = sum(1 for c in contradictions if c.severity == "high")
    moderate = sum(1 for c in contradictions if c.severity == "moderate")
    return {
        "critical": critical,
        "high": high,
        "moderate": moderate,
        "total": len(contradictions),
    }
