import pytest
from sports_signal_bot.context_assembly.context_assemblers import (
    build_governance_context_assembler,
    register_context_assembly_input,
    assemble_governance_context_bundle
)
from sports_signal_bot.context_assembly.sections import build_context_section, SECTION_NO_SAFE_VISIBILITY, SECTION_SOVEREIGNTY_WARNING
from sports_signal_bot.context_assembly.bundles import OUTPUT_BLOCKED, OUTPUT_CURRENT_WITH_CAPS

def test_assemble_context_bundle_missing_no_safe():
    inp = register_context_assembly_input("operator", "ref1", "current", "none", "ok", "active")
    sec = build_context_section("general_section", "content")

    bundle = assemble_governance_context_bundle("operator", [inp], [sec])
    # Should block because no_safe_visibility is required by inputs but missing in sections
    assert bundle.bundle_status == OUTPUT_BLOCKED
    assert "Missing mandatory no_safe_visibility section" in bundle.warnings

def test_assemble_context_bundle_with_no_safe_and_sovereignty():
    inp = register_context_assembly_input("operator", "ref1", "current", "none", "warning", "active")
    sec1 = build_context_section(SECTION_NO_SAFE_VISIBILITY, "content")
    sec2 = build_context_section(SECTION_SOVEREIGNTY_WARNING, "content")

    bundle = assemble_governance_context_bundle("operator", [inp], [sec1, sec2])
    assert bundle.bundle_status == OUTPUT_CURRENT_WITH_CAPS

def test_assemble_context_bundle_stale_input():
    inp = register_context_assembly_input("operator", "ref1", "stale", "none", "ok", "none")
    sec = build_context_section("general_section", "content")

    bundle = assemble_governance_context_bundle("operator", [inp], [sec])
    assert bundle.bundle_status == "stale_context"
