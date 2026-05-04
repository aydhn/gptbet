from .contracts import DebtSettlementDecisionRecord, ConvergenceDebtEntryRecord

def identify_debt_settlement_candidates(entries: list[ConvergenceDebtEntryRecord]) -> list[str]:
    # Dummy logic: any entry not critical might be a candidate
    return [e.debt_entry_id for e in entries if e.debt_severity.level != "critical"]

def validate_debt_settlement(entry: ConvergenceDebtEntryRecord, evidence_exists: bool) -> bool:
    if not evidence_exists:
        return False
    # If the debt is structurally blocking, it cannot be easily settled
    if entry.debt_severity.level == "structurally_blocking":
        return False
    return True

def apply_debt_settlement_decision(entry: ConvergenceDebtEntryRecord, decision: DebtSettlementDecisionRecord):
    if decision.is_settled:
        entry.debt_status = "debt_settled"

def summarize_debt_settlement(decision: DebtSettlementDecisionRecord) -> str:
    status = "Settled" if decision.is_settled else "Pending/Failed"
    return f"Settlement {status}: {decision.resolution_details}"
