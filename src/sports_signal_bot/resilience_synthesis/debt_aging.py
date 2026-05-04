from .contracts import ConvergenceDebtEntryRecord

def age_debt_entries(entries: list[ConvergenceDebtEntryRecord], days: int):
    for entry in entries:
        if entry.debt_age.is_aging:
             entry.debt_age.days_old += days

def escalate_debt_severity_with_age(entry: ConvergenceDebtEntryRecord):
    if entry.debt_age.days_old > 30 and entry.debt_severity.level in ["low", "moderate"]:
        entry.debt_severity.level = "high"
    if entry.debt_age.days_old > 90 and entry.debt_severity.level in ["high", "moderate", "low"]:
        entry.debt_severity.level = "critical"

def classify_debt_severity(severity_level: str) -> str:
    return f"Severity is {severity_level}"

def explain_debt_severity(entry: ConvergenceDebtEntryRecord) -> str:
    return f"Debt {entry.debt_entry_id} is {entry.debt_severity.level} and {entry.debt_age.days_old} days old."
