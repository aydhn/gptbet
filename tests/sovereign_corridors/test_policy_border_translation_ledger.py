from sports_signal_bot.sovereign_corridors.ledgers import append_translation_ledger_entry, verify_translation_ledger_integrity
from sports_signal_bot.sovereign_corridors.contracts import PolicyBorderTranslationLedgerRecord, TranslationLedgerEntryRecord

def test_ledger():
    ledger = PolicyBorderTranslationLedgerRecord(ledger_id="l1", source_region_ref="r1", target_region_ref="r2")
    entry = TranslationLedgerEntryRecord(entry_id="e1", source_element="s1", target_element="t1", mapping_rule="m1", loss_class="no_loss")

    ledger = append_translation_ledger_entry(ledger, entry)
    assert len(ledger.translation_entries) == 1

    assert verify_translation_ledger_integrity(ledger)
    ledger.warnings.append("compromised")
    assert not verify_translation_ledger_integrity(ledger)
