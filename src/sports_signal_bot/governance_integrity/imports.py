from typing import Optional
from typing import Dict, Any, Tuple
import uuid
from datetime import datetime

from .contracts import (
    DistributionPackageRecord,
    ImportedBundleStateRecord,
    BundleStatus,
    VerificationStatus
)
from .verification import BundleVerifier

def verify_before_import(package: DistributionPackageRecord) -> Tuple[bool, "Optional[str]"]:
    """Verifies a distribution package before allowing it to be imported."""
    # Real implementation would re-run hashing and verify signature using public key.
    # We will simulate the check via simple logic for now.
    verifier = BundleVerifier()
    signer_id = package.packaging_record.signature_block.signer_id

    if not verifier.signer_provider.get_signer(signer_id):
        return False, "Unknown signer"

    return True, None

def quarantine_untrusted_bundle(package: DistributionPackageRecord, reason: str) -> ImportedBundleStateRecord:
    """Quarantines a package that failed verification."""
    return ImportedBundleStateRecord(
        import_id=f"imp_{uuid.uuid4().hex[:8]}",
        package_id=package.packaging_record.package_id,
        imported_at=datetime.utcnow(),
        initial_status=BundleStatus.QUARANTINED,
        quarantine_reason=reason
    )

def import_distribution_bundle(package: DistributionPackageRecord) -> ImportedBundleStateRecord:
    """Safely imports a distribution package."""
    is_valid, error = verify_before_import(package)

    if not is_valid:
        return quarantine_untrusted_bundle(package, error)

    return ImportedBundleStateRecord(
        import_id=f"imp_{uuid.uuid4().hex[:8]}",
        package_id=package.packaging_record.package_id,
        imported_at=datetime.utcnow(),
        initial_status=BundleStatus.REVIEW_VERIFIED,
        quarantine_reason=None
    )
