from typing import Dict, Any, Optional
from .contracts import (
    NotarizationRequestRecord,
    NotarizationReceiptRecord,
    NotarizationVerificationRecord,
    NotaryProviderRecord
)
import uuid
import datetime

def build_notarization_digest(target_ref: str, payload: str) -> str:
    import hashlib
    return hashlib.sha256(f"{target_ref}:{payload}".encode()).hexdigest()

def request_notarization(digest: str, provider: str, target_ref: str) -> NotarizationRequestRecord:
    return NotarizationRequestRecord(
        request_id=str(uuid.uuid4()),
        digest=digest,
        notary_provider=provider,
        target_ref=target_ref
    )

def verify_notarization_receipt(receipt: NotarizationReceiptRecord, expected_digest: str) -> NotarizationVerificationRecord:
    status = "notarization_verified" if expected_digest in receipt.receipt_payload else "notarization_unverified"
    return NotarizationVerificationRecord(
        verification_id=str(uuid.uuid4()),
        receipt_id=receipt.receipt_id,
        status=status
    )

def classify_notarization_result(verification: NotarizationVerificationRecord) -> str:
    return verification.status

def summarize_notarization_support(verifications: list[NotarizationVerificationRecord]) -> Dict[str, int]:
    summary = {"notarization_verified": 0, "notarization_unverified": 0}
    for v in verifications:
        if v.status in summary:
            summary[v.status] += 1
    return summary
