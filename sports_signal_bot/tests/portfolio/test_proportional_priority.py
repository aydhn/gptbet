import pytest
import datetime
from sports_signal_bot.portfolio.contracts import PortfolioConfig, PortfolioCandidateRecord
from sports_signal_bot.portfolio.runner import PortfolioRunner

def test_proportional_priority_allocation():
    config = PortfolioConfig(
        default_allocation_strategy="proportional_priority",
        daily_risk_budget_fraction=0.10,
        max_bucket_risk_fraction=0.05,
        same_event_related_market_guard=True
    )
    runner = PortfolioRunner(config)

    dt = datetime.datetime.now(datetime.timezone.utc)
    candidates = [
        PortfolioCandidateRecord(
            event_id="E1",
            event_datetime_utc=dt,
            sport="football",
            market_type="1x2",
            action_class="approved_candidate",
            selected_side="home",
            proposed_stake_fraction=0.03,
            proposed_stake_units=30.0,
            bankroll_before_window=1000.0,
            signal_score=0.8,
            confidence=0.9
        ),
        PortfolioCandidateRecord(
            event_id="E2",
            event_datetime_utc=dt,
            sport="football",
            market_type="1x2",
            action_class="candidate",
            selected_side="home",
            proposed_stake_fraction=0.04,
            proposed_stake_units=40.0,
            bankroll_before_window=1000.0,
            signal_score=0.4,
            confidence=0.8
        )
    ]

    allocations, manifest = runner.allocate(candidates)

    assert len(allocations) == 2

    e1_alloc = next(a for a in allocations if a.event_id == "E1")
    e2_alloc = next(a for a in allocations if a.event_id == "E2")

    # E1 has higher score than E2, so proportion of E1 > proportion of E2
    # Total bucket is 0.05. Both want 0.07. They will be scaled.
    assert e1_alloc.allocated_stake_fraction > e2_alloc.allocated_stake_fraction
    assert e1_alloc.allocation_status.value in ["fully_allocated", "partially_allocated"]
    assert e1_alloc.allocated_stake_fraction <= 0.03
