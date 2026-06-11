from typing import Dict, Any, List
import uuid
from datetime import datetime

from .contracts import (
    LedgerEntryRecord,
    VerificationStatus,
    AppendLedgerEntryParams,
)
from .canonicalization import compute_hash


class TamperEvidentLedger:
    """An append-only hash-chained governance ledger."""

    def __init__(self):
        self.entries: List[LedgerEntryRecord] = []

    def append_ledger_entry(
        self, params: AppendLedgerEntryParams
    ) -> LedgerEntryRecord:
        """Appends a new entry to the ledger hash chain."""
        prev_hash = self.entries[-1].chain_hash if self.entries else None

        entry_payload = {
            "event_family": params.event_family,
            "actor_metadata": params.actor_metadata,
            "bundle_refs": params.bundle_refs,
            "decision_refs": params.decision_refs,
            "proof_refs": params.proof_refs,
            "redacted_payload": params.redacted_payload,
        }
        entry_hash = compute_hash(entry_payload)

        chain_payload = {
            "entry_hash": entry_hash,
            "previous_entry_hash": prev_hash,
        }
        chain_hash = compute_hash(chain_payload)

        entry = LedgerEntryRecord(
            entry_id=f"entry_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            event_family=params.event_family,
            actor_metadata=params.actor_metadata,
            bundle_refs=params.bundle_refs,
            decision_refs=params.decision_refs,
            proof_refs=params.proof_refs,
            verification_status=VerificationStatus.VALID,
            entry_hash=entry_hash,
            previous_entry_hash=prev_hash,
            chain_hash=chain_hash,
            redacted_payload=params.redacted_payload,
        )
        self.entries.append(entry)
        return entry

    def verify_ledger_chain(self) -> bool:
        """Verifies the integrity of the entire ledger chain."""
        for i in range(1, len(self.entries)):
            current = self.entries[i]
            previous = self.entries[i - 1]

            if current.previous_entry_hash != previous.chain_hash:
                return False

            # Recompute entry hash
            entry_payload = {
                "event_family": current.event_family,
                "actor_metadata": current.actor_metadata,
                "bundle_refs": current.bundle_refs,
                "decision_refs": current.decision_refs,
                "proof_refs": current.proof_refs,
                "redacted_payload": current.redacted_payload,
            }
            if compute_hash(entry_payload) != current.entry_hash:
                return False

            # Recompute chain hash
            chain_payload = {
                "entry_hash": current.entry_hash,
                "previous_entry_hash": current.previous_entry_hash,
            }
            if compute_hash(chain_payload) != current.chain_hash:
                return False

        return True

    def summarize_ledger_integrity(self) -> Dict[str, Any]:
        """Summarizes the integrity state of the ledger."""
        is_intact = self.verify_ledger_chain()
        return {
            "entry_count": len(self.entries),
            "is_intact": is_intact,
            "tail_entry_hash": (
                self.entries[-1].chain_hash if self.entries else None
            ),
            "last_verified_at": datetime.utcnow().isoformat(),
        }


# Global instance for demonstration
_global_ledger = TamperEvidentLedger()


def get_ledger() -> TamperEvidentLedger:
    return _global_ledger
