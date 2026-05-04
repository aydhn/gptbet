import pytest
from sports_signal_bot.governance_health import (
    build_stabilization_program_portfolio,
    register_portfolio_entry,
    compute_portfolio_burden,
    prioritize_portfolio_entries,
    summarize_portfolio_state
)

def test_portfolio_creation():
    portfolio = build_stabilization_program_portfolio(
        "quorum_stabilization_portfolio",
        "policy_1",
        "policy_2",
        "policy_3"
    )
    assert portfolio.portfolio_family == "quorum_stabilization_portfolio"
    assert portfolio.health_status == "initializing"

def test_portfolio_entry_registration():
    portfolio = build_stabilization_program_portfolio(
        "quorum_stabilization_portfolio", "p1", "p2", "p3"
    )
    entry = register_portfolio_entry(
        portfolio,
        "prog_ref",
        "primary_recovery_entry",
        "stage_ref",
        "stabilization_critical"
    )
    assert entry.portfolio_role == "primary_recovery_entry"
    assert len(portfolio.entry_refs) == 1

def test_portfolio_burden_and_summary():
    portfolio = build_stabilization_program_portfolio(
        "quorum_stabilization_portfolio", "p1", "p2", "p3"
    )
    entry1 = register_portfolio_entry(portfolio, "ref1", "primary_recovery_entry", "s1", "stabilization_critical")
    entry2 = register_portfolio_entry(portfolio, "ref2", "support_recovery_entry", "s2", "review_only_support")

    entry1.portfolio_status = "portfolio_replay_heavy"
    entry2.portfolio_status = "portfolio_balanced"

    summary = summarize_portfolio_state(portfolio, [entry1, entry2])
    assert summary["health_status"] == "backlogged"
    assert summary["burdens"]["replay_heavy"] == 1
