from typing import List

from .contracts import (
    ConvergenceDebtLedgerRecord,
    ConvergenceDebtEntryRecord,
    ConvergenceDebtHealthRecord,
    DebtAgeRecord,
    DebtSeverityRecord
)

def build_convergence_debt_ledger(ledger_id: str, family: str) -> ConvergenceDebtLedgerRecord:
    return ConvergenceDebtLedgerRecord(
        convergence_debt_ledger_id=ledger_id,
        ledger_family=family,
        health_status=ConvergenceDebtHealthRecord(
            health_id=f"h_{ledger_id}",
            status="healthy"
        )
    )

def register_convergence_debt_entry(
    ledger: ConvergenceDebtLedgerRecord,
    entry_id: str,
    family: str,
    severity: str
) -> ConvergenceDebtEntryRecord:
    entry = ConvergenceDebtEntryRecord(
        debt_entry_id=entry_id,
        debt_family=family,
        debt_severity=DebtSeverityRecord(severity_id=f"sev_{entry_id}", level=severity),
        debt_age=DebtAgeRecord(age_id=f"age_{entry_id}", days_old=0, is_aging=True),
        debt_status="debt_open",
        bounded_effect_summary="Registered new debt"
    )
    ledger.active_debt_entry_refs.append(entry_id)
    return entry

def summarize_convergence_debt_ledger(ledger: ConvergenceDebtLedgerRecord) -> dict:
    return {
        "id": ledger.convergence_debt_ledger_id,
        "family": ledger.ledger_family,
        "active_debts": len(ledger.active_debt_entry_refs),
        "settled_debts": len(ledger.settled_debt_entry_refs),
        "health": ledger.health_status.status
    }
