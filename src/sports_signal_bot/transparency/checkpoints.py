import hashlib
from typing import List, Optional
from datetime import datetime
from .contracts import (
    TransparencyCheckpointRecord, CheckpointSignatureRecord, CheckpointTrustRecord,
    CheckpointVerificationRecord, VerificationStatus, TrustStatus
)

class CheckpointManager:
    def __init__(self):
        self._signatures = {}

    def sign_checkpoint(self, checkpoint: TransparencyCheckpointRecord, signer_set: List[str], signature_block: str, scope: str = "global") -> CheckpointSignatureRecord:
        sig = CheckpointSignatureRecord(
            signature_id=f"sig_{datetime.utcnow().timestamp()}",
            checkpoint_id=checkpoint.checkpoint_id,
            signer_set=signer_set,
            signature_block=signature_block,
            checkpoint_scope=scope
        )
        self._signatures[checkpoint.checkpoint_id] = sig
        checkpoint.signed_checkpoint_ref = sig.signature_id
        return sig

    def verify_signed_checkpoint(self, checkpoint: TransparencyCheckpointRecord) -> CheckpointVerificationRecord:
        sig = self._signatures.get(checkpoint.checkpoint_id)
        if not sig:
            return CheckpointVerificationRecord(
                verification_id=f"ver_{datetime.utcnow().timestamp()}",
                checkpoint_id=checkpoint.checkpoint_id,
                status=VerificationStatus.FAILED
            )

        # Dummy signature verification
        is_valid = bool(sig.signature_block)

        return CheckpointVerificationRecord(
            verification_id=f"ver_{datetime.utcnow().timestamp()}",
            checkpoint_id=checkpoint.checkpoint_id,
            status=VerificationStatus.VERIFIED if is_valid else VerificationStatus.FAILED
        )

    def validate_checkpoint_trust(self, checkpoint: TransparencyCheckpointRecord) -> CheckpointTrustRecord:
        ver_rec = self.verify_signed_checkpoint(checkpoint)
        status = TrustStatus.TRUSTED if ver_rec.status == VerificationStatus.VERIFIED else TrustStatus.UNTRUSTED
        return CheckpointTrustRecord(
            trust_id=f"trust_{datetime.utcnow().timestamp()}",
            checkpoint_id=checkpoint.checkpoint_id,
            trust_status=status
        )
