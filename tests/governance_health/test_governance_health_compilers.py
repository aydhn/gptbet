import pytest
from sports_signal_bot.governance_health import (
    build_governance_health_compiler,
    register_compiler_input,
    execute_health_compiler_passes,
    compute_compiler_band,
    summarize_compiler_state
)

def test_compiler_creation():
    compiler = build_governance_health_compiler("stabilization_portfolio_health_compiler")
    assert compiler.compiler_family == "stabilization_portfolio_health_compiler"

def test_compiler_passes_and_band():
    compiler = build_governance_health_compiler("stabilization_portfolio_health_compiler")
    i1 = register_compiler_input(compiler, "family1", "ref1", "current", "none", "matched", "intact", "applicable")
    i2 = register_compiler_input(compiler, "family2", "ref2", "stale", "none", "matched", "intact", "applicable")

    passes = execute_health_compiler_passes(compiler, [i1, i2])
    assert len(passes) == 2
    assert any(p.pass_type == "currentness_pass" and p.status == "failed" for p in passes)

    output = compute_compiler_band(passes, [])
    assert output.health_band == "review_only_health"
    assert output.restoration_ceiling == "low"

def test_compiler_summary():
    compiler = build_governance_health_compiler("stabilization_portfolio_health_compiler")
    i1 = register_compiler_input(compiler, "family1", "ref1", "current", "none", "matched", "intact", "applicable")
    passes = execute_health_compiler_passes(compiler, [i1])
    output = compute_compiler_band(passes, [])

    summary = summarize_compiler_state(compiler, passes, output)
    assert summary["state"] == "passed"
    assert summary["health_band"] == "strong_bounded_health"
