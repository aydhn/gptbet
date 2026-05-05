import pytest
from sports_signal_bot.hardening.ci import evaluate_release_blockers

def test_evaluate_release_blockers_none():
    blockers = evaluate_release_blockers({"critical_violations": 0}, {"status": "stable"})
    assert len(blockers) == 0

def test_evaluate_release_blockers_some():
    blockers = evaluate_release_blockers({"critical_violations": 1}, {"status": "flaky"})
    assert len(blockers) == 2
