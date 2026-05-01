from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from .contracts import LedgerEntryRecord, VerificationStatus
from .canonicalization import compute_hash

class TamperEvidentLedger:
    """An append-only hash-chained governance ledger."""
    def __init__(self):
        self.entries: List[LedgerEntryRecord] = []

    def append_ledger_entry(
        self,
        event_family: str,
        actor_metadata: Dict[str, Any],
        bundle_refs: List[str] = None,
        decision_refs: List[str] = None,
        proof_refs: List[str] = None,
        redacted_payload: Dict[str, Any] = None
    ) -> LedgerEntryRecord:
        """Appends a new entry to the ledger hash chain."""
        previous_entry_hash = self.entries[-1].chain_hash if self.entries else None

        entry_payload = {
            "event_family": event_family,
            "actor_metadata": actor_metadata,
            "bundle_refs": bundle_refs or [],
            "decision_refs": decision_refs or [],
            "proof_refs": proof_refs or [],
            "redacted_payload": redacted_payload or {}
        }
        entry_hash = compute_hash(entry_payload)

        chain_payload = {
            "entry_hash": entry_hash,
            "previous_entry_hash": previous_entry_hash
        }
        chain_hash = compute_hash(chain_payload)

        entry = LedgerEntryRecord(
            entry_id=f"entry_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            event_family=event_family,
            actor_metadata=actor_metadata,
            bundle_refs=bundle_refs or [],
            decision_refs=decision_refs or [],
            proof_refs=proof_refs or [],
            verification_status=VerificationStatus.VALID,
            entry_hash=entry_hash,
            previous_entry_hash=previous_entry_hash,
            chain_hash=chain_hash,
            redacted_payload=redacted_payload or {}
        )
        self.entries.append(entry)
        return entry

    def verify_ledger_chain(self) -> bool:
        """Verifies the integrity of the entire ledger chain."""
        for i in range(1, len(self.entries)):
            current = self.entries[i]
            previous = self.entries[i-1]

            if current.previous_entry_hash != previous.chain_hash:
                return False

            # Recompute entry hash
            entry_payload = {
                "event_family": current.event_family,
                "actor_metadata": current.actor_metadata,
                "bundle_refs": current.bundle_refs,
                "decision_refs": current.decision_refs,
                "proof_refs": current.proof_refs,
                "redacted_payload": current.redacted_payload
            }
            if compute_hash(entry_payload) != current.entry_hash:
                return False

            # Recompute chain hash
            chain_payload = {
                "entry_hash": current.entry_hash,
                "previous_entry_hash": current.previous_entry_hash
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
            "tail_entry_hash": self.entries[-1].chain_hash if self.entries else None,
            "last_verified_at": datetime.utcnow().isoformat()
        }

# Global instance for demonstration
_global_ledger = TamperEvidentLedger()

def get_ledger() -> TamperEvidentLedger:
    return _global_ledger
