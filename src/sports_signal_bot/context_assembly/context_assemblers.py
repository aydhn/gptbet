import uuid
from typing import List
from .contracts import (
    SovereignGovernanceContextAssemblerRecord,
    ContextAssemblyInputRecord,
    ContextBundleRecord,
    ContextSectionRecord
)
from .bundles import classify_context_bundle_output, OUTPUT_BLOCKED
from .sections import SECTION_NO_SAFE_VISIBILITY, SECTION_SOVEREIGNTY_WARNING

def build_governance_context_assembler(family: str) -> SovereignGovernanceContextAssemblerRecord:
    return SovereignGovernanceContextAssemblerRecord(
        context_assembler_id=f"sgea_{uuid.uuid4().hex[:8]}",
        assembler_family=family,
        input_refs=[],
        bundle_refs=[],
        section_refs=[],
        verification_refs=[],
        audience_profile_refs=["operator", "reviewer", "executive"],
        health_status="healthy"
    )

def register_context_assembly_input(family: str, source_ref: str, currentness: str, caveats: str, sovereignty: str, no_safe: str) -> ContextAssemblyInputRecord:
    return ContextAssemblyInputRecord(
        input_id=f"inp_{uuid.uuid4().hex[:8]}",
        input_family=family,
        source_ref=source_ref,
        currentness_state=currentness,
        caveat_state=caveats,
        sovereignty_state=sovereignty,
        no_safe_visibility_state=no_safe
    )

def assemble_governance_context_bundle(
    audience: str,
    inputs: List[ContextAssemblyInputRecord],
    sections: List[ContextSectionRecord],
    force_block: bool = False
) -> ContextBundleRecord:

    # Rule: no-safe and sovereignty sections mandatory if applicable in inputs
    needs_no_safe = any(i.no_safe_visibility_state == "active" for i in inputs)
    has_no_safe = any(s.family == SECTION_NO_SAFE_VISIBILITY for s in sections)

    needs_sovereignty = any(i.sovereignty_state in ["warning", "blocked"] for i in inputs)
    has_sovereignty = any(s.family == SECTION_SOVEREIGNTY_WARNING for s in sections)

    status = classify_context_bundle_output(inputs)

    warnings = []
    if needs_no_safe and not has_no_safe:
        status = OUTPUT_BLOCKED
        warnings.append("Missing mandatory no_safe_visibility section")

    if needs_sovereignty and not has_sovereignty:
        status = OUTPUT_BLOCKED
        warnings.append("Missing mandatory sovereignty_warning section")

    if force_block:
         status = OUTPUT_BLOCKED

    bundle = ContextBundleRecord(
        context_bundle_id=f"cb_{uuid.uuid4().hex[:8]}",
        bundle_family="default_bundle",
        target_audience=audience,
        included_section_refs=[s.section_id for s in sections],
        included_evidence_refs=[],
        included_trace_refs=[],
        currentness_state="computed",
        bundle_status=status
    )
    bundle.warnings.extend(warnings)
    return bundle

def verify_context_bundle_against_inputs(bundle: ContextBundleRecord, inputs: List[ContextAssemblyInputRecord]) -> bool:
    if bundle.bundle_status == OUTPUT_BLOCKED:
        return False
    return True

def summarize_context_bundle(bundle: ContextBundleRecord) -> str:
    return f"Bundle {bundle.context_bundle_id} -> {bundle.bundle_status}"
