from typing import Dict, Any, List
import uuid

from .contracts import (
    SignedBundleRecord,
    DistributionPackageRecord,
    BundlePackagingRecord,
    SignatureRecord,
    BundleManifestRecord,
    TrustLevel
)

def build_distribution_package(
    bundle: SignedBundleRecord,
    payload: Dict[str, Any],
    signature_blob: str,
    required_trust: TrustLevel = TrustLevel.ACTIVE
) -> DistributionPackageRecord:
    """Builds a distribution-ready package for a signed policy bundle."""
    manifest = BundleManifestRecord(
        bundle_family=bundle.bundle_family,
        bundle_version=bundle.bundle_version,
        payload_hash=bundle.bundle_hash,
        created_at=bundle.created_at
    )

    sig_record = SignatureRecord(
        signature_id=bundle.signature_ref,
        signer_id=bundle.signer_id,
        signature_blob=signature_blob,
        algorithm="HMAC-SHA256",
        timestamp=bundle.created_at
    )

    packaging = BundlePackagingRecord(
        package_id=f"pkg_{uuid.uuid4().hex[:8]}",
        package_type="single_bundle_package",
        payload=payload,
        manifest=manifest,
        signature_block=sig_record,
        compatibility_notes="Compatible with v1+ evaluation engine"
    )

    return DistributionPackageRecord(
        distribution_id=f"dist_{uuid.uuid4().hex[:8]}",
        packaging_record=packaging,
        required_trust_level=required_trust,
        import_instructions="verify before import",
        verification_summary={"pre_flight_checked": True}
    )
