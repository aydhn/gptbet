import uuid
from typing import List
from .contracts import (
    ContextBundleRecord,
    ContextAssemblyInputRecord,
    ContextSectionRecord
)
from .sections import SECTION_NO_SAFE_VISIBILITY, SECTION_SOVEREIGNTY_WARNING

OUTPUT_CURRENT_WITH_CAPS = "current_context_with_caps"
OUTPUT_CAVEATED = "caveated_context"
OUTPUT_REVIEW_ONLY = "review_only_context"
OUTPUT_DEGRADED = "degraded_context"
OUTPUT_BLOCKED = "blocked_context"
OUTPUT_STALE = "stale_context"

def classify_context_bundle_output(inputs: List[ContextAssemblyInputRecord]) -> str:
    # Rule: stale inputs -> stale bundle
    if any(i.currentness_state == "stale" for i in inputs):
        return OUTPUT_STALE

    if any(i.sovereignty_state == "blocked" for i in inputs):
         return OUTPUT_BLOCKED

    if any(i.currentness_state == "degraded" for i in inputs):
        return OUTPUT_DEGRADED

    if any(i.caveat_state == "caveated" for i in inputs):
        return OUTPUT_CAVEATED

    return OUTPUT_CURRENT_WITH_CAPS

def attach_context_caveats(bundle: ContextBundleRecord, caveats: List[str]):
    bundle.warnings.extend(caveats)

def preserve_no_safe_context_sections(sections: List[ContextSectionRecord]) -> bool:
    has_no_safe = any(s.family == SECTION_NO_SAFE_VISIBILITY for s in sections)
    has_sovereignty = any(s.family == SECTION_SOVEREIGNTY_WARNING for s in sections)
    return has_no_safe and has_sovereignty

def explain_context_assembly(bundle: ContextBundleRecord) -> str:
    return f"Context Bundle {bundle.context_bundle_id} targeting {bundle.target_audience}. Status: {bundle.bundle_status}"
