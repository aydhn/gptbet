import pytest
from sports_signal_bot.assurance.conflicts import resolve_conflict_precedence

def test_claim_conflict():
    assert resolve_conflict_precedence({}) == "resolved"
