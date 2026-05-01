import hashlib
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .contracts import (
    TransparencyEntryRecord, TransparencyLogRecord, TransparencyCheckpointRecord,
    LogFamily, EventFamily, InclusionStatus, InclusionProofRecord, VerificationStatus,
    ConsistencyProofRecord
)
from .merkle import compute_merkle_root, build_inclusion_proof, verify_inclusion_proof, build_consistency_proof

class TransparencyLogManager:
    def __init__(self):
        self._logs: Dict[LogFamily, TransparencyLogRecord] = {}

    def get_log(self, family: LogFamily) -> TransparencyLogRecord:
        if family not in self._logs:
            self._logs[family] = TransparencyLogRecord(
                log_id=f"log_{family.value}",
                family=family
            )
        return self._logs[family]

    def compute_entry_hash(self, payload_hash: str, prior_hash: Optional[str]) -> str:
        data = f"{payload_hash}:{prior_hash or ''}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def append_transparency_entry(self, family: LogFamily, event_family: EventFamily, event_ref: str, payload_hash: str) -> TransparencyEntryRecord:
        log = self.get_log(family)

        prior_hash = log.entries[-1].event_hash if log.entries else None
        event_hash = self.compute_entry_hash(payload_hash, prior_hash)

        entry = TransparencyEntryRecord(
            transparency_entry_id=f"entry_{datetime.utcnow().timestamp()}",
            log_family=family,
            event_family=event_family,
            event_ref=event_ref,
            event_hash=event_hash,
            payload_hash=payload_hash,
            prior_entry_hash=prior_hash,
            log_index=len(log.entries),
            inclusion_status=InclusionStatus.PENDING
        )
        log.entries.append(entry)
        return entry

    def seal_transparency_checkpoint(self, family: LogFamily) -> TransparencyCheckpointRecord:
        log = self.get_log(family)
        if not log.entries:
            raise ValueError("Cannot seal checkpoint for empty log")

        tree_size = len(log.entries)
        leaves = [e.event_hash for e in log.entries]
        root_hash = compute_merkle_root(leaves)

        prior_ref = log.checkpoints[-1].checkpoint_id if log.checkpoints else None

        checkpoint = TransparencyCheckpointRecord(
            checkpoint_id=f"cp_{datetime.utcnow().timestamp()}",
            log_id=log.log_id,
            tree_size=tree_size,
            root_hash=root_hash,
            prior_checkpoint_ref=prior_ref
        )

        for entry in log.entries:
            if entry.inclusion_status == InclusionStatus.PENDING:
                entry.inclusion_status = InclusionStatus.INCLUDED

        log.checkpoints.append(checkpoint)
        return checkpoint

    def get_inclusion_proof(self, family: LogFamily, entry_index: int) -> InclusionProofRecord:
        log = self.get_log(family)
        if entry_index < 0 or entry_index >= len(log.entries):
            raise ValueError("Invalid entry index")

        if not log.checkpoints:
            raise ValueError("No checkpoints sealed")

        latest_cp = log.checkpoints[-1]
        leaves = [e.event_hash for e in log.entries[:latest_cp.tree_size]]
        path = build_inclusion_proof(leaves, entry_index)

        return InclusionProofRecord(
            proof_id=f"inc_{datetime.utcnow().timestamp()}",
            log_id=log.log_id,
            tree_size=latest_cp.tree_size,
            leaf_index=entry_index,
            leaf_hash=leaves[entry_index],
            merkle_path=path,
            checkpoint_ref=latest_cp.checkpoint_id,
            verification_status=VerificationStatus.UNVERIFIED
        )

    def get_consistency_proof(self, family: LogFamily, old_tree_size: int, new_tree_size: int) -> ConsistencyProofRecord:
        log = self.get_log(family)
        if old_tree_size > new_tree_size or new_tree_size > len(log.entries):
            raise ValueError("Invalid tree sizes")

        leaves = [e.event_hash for e in log.entries[:new_tree_size]]
        path = build_consistency_proof(leaves, old_tree_size)

        old_root = compute_merkle_root([e.event_hash for e in log.entries[:old_tree_size]])
        new_root = compute_merkle_root(leaves)

        return ConsistencyProofRecord(
            proof_id=f"cons_{datetime.utcnow().timestamp()}",
            log_id=log.log_id,
            old_tree_size=old_tree_size,
            new_tree_size=new_tree_size,
            old_root_hash=old_root,
            new_root_hash=new_root,
            merkle_path=path,
            verification_status=VerificationStatus.UNVERIFIED
        )
