import pytest
from sports_signal_bot.conformance.lint import lint_policy_bundle, SeverityLevel

def test_lint_policy_bundle_ambiguous():
    policy = {"has_ambiguous_precedence": True}
    res = lint_policy_bundle(policy)
    assert not res.passed
    assert any(f.severity == SeverityLevel.CRITICAL for f in res.findings)

def test_lint_policy_bundle_clean():
    policy = {"has_ambiguous_precedence": False, "overlay_widens_scope": False}
    res = lint_policy_bundle(policy)
    assert res.passed
    assert len(res.findings) == 0
