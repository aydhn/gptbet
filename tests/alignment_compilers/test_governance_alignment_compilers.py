import pytest
from sports_signal_bot.alignment_compilers.alignment_compilers import (
    build_governance_alignment_compiler,
    register_alignment_input,
    execute_alignment_compiler_passes,
    compute_alignment_band,
    AlignmentInputRecord
)

def test_build_compiler():
    compiler = build_governance_alignment_compiler("comp-1", "composite_governance_alignment_compiler")
    assert compiler.alignment_compiler_id == "comp-1"

def test_register_input():
    compiler = build_governance_alignment_compiler("comp-1", "family")
    inp = AlignmentInputRecord("inp-1", "family", "src", "stale", "caveated", "passed", "visible")
    register_alignment_input(compiler, inp)
    assert len(compiler.input_refs) == 1
    assert len(compiler.warnings) == 1

def test_execute_passes():
    compiler = build_governance_alignment_compiler("comp-1", "family")
    inp = AlignmentInputRecord("inp-1", "family", "src", "current", "none", "passed", "hidden")
    passes = execute_alignment_compiler_passes(compiler, [inp])
    assert len(passes) == 2
    assert any(p.pass_type == "no_safe_visibility_pass" and p.result == "failed" for p in passes)

def test_compute_band():
    band = compute_alignment_band([], [], [])
    assert band == "strong_bounded_alignment"
