import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any, Tuple
import uuid

from .contracts import SignatureRecord
from .canonicalization import canonicalize_for_signing

def _sign_payload(payload: Dict[str, Any], signer_id: str, dummy_key: str) -> SignatureRecord:
    """
    Creates an HMAC signature for a payload using a dummy key for local testing.
    In production, this would use a real KMS or hardware-backed key.
    """
    canonical_bytes = canonicalize_for_signing(payload)
    signature_bytes = hmac.new(
        dummy_key.encode('utf-8'),
        canonical_bytes,
        hashlib.sha256
    ).digest()

    return SignatureRecord(
        signature_id=f"sig_{uuid.uuid4().hex[:8]}",
        signer_id=signer_id,
        signature_blob=signature_bytes.hex(),
        algorithm="HMAC-SHA256",
        timestamp=datetime.utcnow()
    )

def sign_payload_with_local_key(payload: Dict[str, Any], signer_id: str) -> SignatureRecord:
    """Signs a payload using a derived local key placeholder."""
    # Dummy key generation based on signer_id
    dummy_key = f"dummy_key_for_{signer_id}"
    return _sign_payload(payload, signer_id, dummy_key)

def verify_signature(payload: Dict[str, Any], signature_record: SignatureRecord) -> bool:
    """
    Verifies the HMAC signature.
    In production, this would use public keys or an external verification service.
    """
    if signature_record.algorithm != "HMAC-SHA256":
        return False

    dummy_key = f"dummy_key_for_{signature_record.signer_id}"
    expected_record = _sign_payload(payload, signature_record.signer_id, dummy_key)

    return hmac.compare_digest(
        signature_record.signature_blob,
        expected_record.signature_blob
    )
