from typing import Dict, Any, List
from sports_signal_bot.sovereign_corridors.contracts import (
    PolicyBorderTranslationLedgerRecord,
    TranslationLedgerEntryRecord
)

def append_translation_ledger_entry(
    ledger: PolicyBorderTranslationLedgerRecord,
    entry: TranslationLedgerEntryRecord
) -> PolicyBorderTranslationLedgerRecord:
    ledger.translation_entries.append({
        "entry_id": entry.entry_id,
        "source": entry.source_element,
        "target": entry.target_element,
        "loss_class": entry.loss_class
    })
    ledger.active_mappings.append(entry.entry_id)
    return ledger

def verify_translation_ledger_integrity(ledger: PolicyBorderTranslationLedgerRecord) -> bool:
    if "compromised" in ledger.warnings:
        return False
    return True

def replay_translation_ledger_entry(entry: Dict[str, Any]) -> str:
    # mock replay
    return "replay_matched"

def summarize_translation_ledger(ledger: PolicyBorderTranslationLedgerRecord) -> Dict[str, Any]:
    return {
        "ledger_id": ledger.ledger_id,
        "entry_count": len(ledger.translation_entries),
        "active_mappings": len(ledger.active_mappings),
        "warnings": len(ledger.warnings)
    }
