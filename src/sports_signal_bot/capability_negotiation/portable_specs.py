import uuid
from typing import List, Dict, Any

from sports_signal_bot.capability_negotiation.contracts import (
    PortableSpecBundleRecord,
    SpecPortabilityClass,
    PortableAssertionRecord,
    SpecExportConstraintRecord
)

def filter_nonportable_specs(raw_specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [s for s in raw_specs if not s.get("internal_only", False)]

def build_portable_spec_bundle(
    bundle_family: str,
    raw_specs: List[Dict[str, Any]],
    assertions: List[Dict[str, str]],
    redaction_profile: str
) -> PortableSpecBundleRecord:

    portable_specs = filter_nonportable_specs(raw_specs)

    portability_class = SpecPortabilityClass.fully_portable
    if any(s.get("requires_review", False) for s in portable_specs):
        portability_class = SpecPortabilityClass.review_only_portable

    export_constraints = []
    if portability_class == SpecPortabilityClass.review_only_portable:
        export_constraints.append(SpecExportConstraintRecord(constraint="manual_review_required_prior_to_import"))

    portable_assertions = [
        PortableAssertionRecord(assertion_id=a["id"], semantics=a["semantics"])
        for a in assertions
    ]

    return PortableSpecBundleRecord(
        spec_bundle_id=str(uuid.uuid4()),
        bundle_family=bundle_family,
        portable_profile=portability_class,
        included_specs=[s["spec_id"] for s in portable_specs],
        included_assertions=portable_assertions,
        version_matrix={"core": "1.0.0"},
        compatibility_notes=["Exported for federated verification"],
        export_constraints=export_constraints,
        redaction_profile=redaction_profile
    )

def verify_portable_spec_bundle(bundle: PortableSpecBundleRecord) -> bool:
    if not bundle.included_specs:
        return False
    if bundle.portable_profile == SpecPortabilityClass.nonportable_internal_only:
        return False
    return True
