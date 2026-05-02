import pytest
from sports_signal_bot.assurance.reporting import generate_assurance_summary

def test_reporting_hooks():
    summary = generate_assurance_summary([{}, {}], [{}])
    assert summary["total_claims"] == 2
