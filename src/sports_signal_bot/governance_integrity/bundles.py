from typing import Dict, Any, List
import uuid
from datetime import datetime

from .contracts import (
    SignedBundleRecord,
    BundleManifestRecord,
    BundleStatus,
    SignerRecord,
    TrustLevel
)
from .canonicalization import compute_bundle_hash, compute_manifest_hash
from .signing import sign_payload_with_local_key

def build_signed_policy_bundle(
    payload: Dict[str, Any],
    bundle_family: str,
    bundle_version: str,
    signer_id: str,
    dependencies: List[str] = None
) -> SignedBundleRecord:
    """Builds a signed policy bundle."""
    # 1. Hash the payload
    payload_hash = compute_bundle_hash(payload)

    # 2. Build the manifest
    manifest = BundleManifestRecord(
        bundle_family=bundle_family,
        bundle_version=bundle_version,
        payload_hash=payload_hash,
        created_at=datetime.utcnow(),
        dependencies=dependencies or []
    )
    manifest_hash = compute_manifest_hash(manifest.model_dump())

    # 3. Sign the manifest hash + payload hash combined
    signing_payload = {
        "payload_hash": payload_hash,
        "manifest_hash": manifest_hash,
        "bundle_family": bundle_family,
        "bundle_version": bundle_version
    }
    signature_record = sign_payload_with_local_key(signing_payload, signer_id)

    # 4. Construct the SignedBundleRecord
    return SignedBundleRecord(
        signed_bundle_id=f"bundle_{uuid.uuid4().hex[:8]}",
        bundle_family=bundle_family,
        bundle_version=bundle_version,
        bundle_hash=payload_hash,
        manifest_hash=manifest_hash,
        signer_id=signer_id,
        signature_ref=signature_record.signature_id,
        created_at=datetime.utcnow(),
        scope={"target": "global"},
        status=BundleStatus.DRAFT_SIGNED
    )

def summarize_bundle_integrity(bundle: SignedBundleRecord) -> Dict[str, Any]:
    """Summarizes the integrity state of a signed bundle."""
    return {
        "bundle_id": bundle.signed_bundle_id,
        "family": bundle.bundle_family,
        "status": bundle.status.value,
        "signer_id": bundle.signer_id,
        "signature_ref": bundle.signature_ref,
        "is_signed": True,
        "warnings": bundle.warnings
    }
