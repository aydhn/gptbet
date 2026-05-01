from datetime import datetime
from typing import Dict, Optional, List
from .contracts import (
    MirrorRecord, MirrorSyncRecord, MirrorVerificationRecord, TrustStatus, VerificationStatus,
    TransparencyCheckpointRecord, LogFamily
)

class MirrorManager:
    def __init__(self):
        self._mirrors: Dict[str, MirrorRecord] = {}

    def create_verification_mirror(self, family: str, source_log_id: str) -> MirrorRecord:
        mirror_id = f"mirror_{family}_{datetime.utcnow().timestamp()}"
        mirror = MirrorRecord(
            mirror_id=mirror_id,
            mirror_family=family,
            source_log_id=source_log_id,
            sync_status="initialized",
            trust_status=TrustStatus.REVIEW_REQUIRED
        )
        self._mirrors[mirror_id] = mirror
        return mirror

    def sync_mirror_from_source(self, mirror_id: str, checkpoint: TransparencyCheckpointRecord) -> MirrorSyncRecord:
        mirror = self._mirrors.get(mirror_id)
        if not mirror:
            raise ValueError("Mirror not found")

        # Simplified sync logic: update mirror's seen checkpoint
        mirror.latest_seen_checkpoint = checkpoint.checkpoint_id
        mirror.latest_verified_tree_size = checkpoint.tree_size
        mirror.sync_status = "synced"

        return MirrorSyncRecord(
            sync_id=f"sync_{datetime.utcnow().timestamp()}",
            mirror_id=mirror_id,
            source_checkpoint_ref=checkpoint.checkpoint_id,
            status="completed"
        )

    def verify_mirror_checkpoint(self, mirror_id: str, checkpoint: TransparencyCheckpointRecord) -> MirrorVerificationRecord:
        mirror = self._mirrors.get(mirror_id)
        if not mirror:
            raise ValueError("Mirror not found")

        if mirror.latest_seen_checkpoint != checkpoint.checkpoint_id:
            mirror.trust_status = TrustStatus.QUARANTINED
            return MirrorVerificationRecord(
                verification_id=f"ver_{datetime.utcnow().timestamp()}",
                mirror_id=mirror_id,
                status=VerificationStatus.FAILED
            )

        mirror.trust_status = TrustStatus.TRUSTED
        return MirrorVerificationRecord(
            verification_id=f"ver_{datetime.utcnow().timestamp()}",
            mirror_id=mirror_id,
            status=VerificationStatus.VERIFIED
        )

    def detect_mirror_divergence(self, mirror_id: str, current_tree_size: int) -> bool:
        mirror = self._mirrors.get(mirror_id)
        if not mirror:
            return False
        # Divergence exists if mirror is ahead of local tree size or stuck far behind
        return mirror.latest_verified_tree_size > current_tree_size
