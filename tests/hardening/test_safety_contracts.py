import pytest
from sports_signal_bot.hardening.safety_contracts import validate_safety_invariants

def test_validate_safety_invariants_healthy():
    state = {"no_safe_visibility": True, "sovereignty_preserved": True}
    run = validate_safety_invariants("mod1", state)
    assert run.status == "healthy"
    assert len(run.violations) == 0

def test_validate_safety_invariants_violated():
    state = {"no_safe_visibility": False, "sovereignty_preserved": False}
    run = validate_safety_invariants("mod1", state)
    assert run.status == "violated"
    assert len(run.violations) == 2
