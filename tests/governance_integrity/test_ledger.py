from sports_signal_bot.governance_integrity.ledger import TamperEvidentLedger
from sports_signal_bot.governance_integrity.contracts import (
    AppendLedgerEntryParams,
)


def test_ledger_append_and_verify():
    ledger = TamperEvidentLedger()
    ledger.append_ledger_entry(
        AppendLedgerEntryParams(
            event_family="test_event", actor_metadata={"actor": "admin"}
        )
    )
    ledger.append_ledger_entry(
        AppendLedgerEntryParams(
            event_family="test_event_2", actor_metadata={"actor": "system"}
        )
    )

    assert len(ledger.entries) == 2
    assert ledger.verify_ledger_chain() is True

    # Tamper with the ledger
    ledger.entries[0].chain_hash = "tampered"
    assert ledger.verify_ledger_chain() is False
