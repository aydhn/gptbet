from .contracts import (
    ClosureBundleRecord, BundleFamily, BundleStatus,
    ClosureBundleSectionRecord, ClosureBundleWarningRecord
)
from typing import List, Dict, Any
import uuid

def build_closure_bundle(family: BundleFamily, sections: List[ClosureBundleSectionRecord]) -> ClosureBundleRecord:
    warnings = []

    # Validation logic to ensure bundles preserve truth
    has_no_safe = any(s.section_family.value == "no_safe_visibility_section" for s in sections)
    has_sovereignty = any(s.section_family.value == "sovereignty_visibility_section" for s in sections)

    if not has_no_safe:
        warnings.append(ClosureBundleWarningRecord(warning_id=str(uuid.uuid4()), message="Missing no-safe visibility section"))
    if not has_sovereignty:
        warnings.append(ClosureBundleWarningRecord(warning_id=str(uuid.uuid4()), message="Missing sovereignty visibility section"))

    status = BundleStatus.bundle_verified
    if warnings:
        status = BundleStatus.bundle_caveated

    return ClosureBundleRecord(
        closure_bundle_id=str(uuid.uuid4()),
        bundle_family=family,
        section_refs=sections,
        bundle_status=status,
        warnings=warnings
    )

def summarize_closure_bundle(bundle: ClosureBundleRecord) -> Dict[str, Any]:
    return {
        "bundle_id": bundle.closure_bundle_id,
        "family": bundle.bundle_family.value,
        "status": bundle.bundle_status.value,
        "section_count": len(bundle.section_refs),
        "warning_count": len(bundle.warnings)
    }
