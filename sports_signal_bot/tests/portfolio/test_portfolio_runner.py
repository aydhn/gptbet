import pytest
import datetime
from sports_signal_bot.portfolio.contracts import PortfolioConfig, PortfolioCandidateRecord
from sports_signal_bot.portfolio.runner import PortfolioRunner

def test_sequential_cap_allocation():
    config = PortfolioConfig(
        default_allocation_strategy="sequential_cap",
        daily_risk_budget_fraction=0.10,
        max_bucket_risk_fraction=0.05,
        same_event_related_market_guard=True
    )
    runner = PortfolioRunner(config)

    dt = datetime.datetime.utcnow()
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
            signal_score=0.7,
            confidence=0.8
        )
    ]

    allocations, manifest = runner.allocate(candidates)

    assert len(allocations) == 2
    # Proposed total is 0.07. Bucket limit is 0.05.
    # The first one (E1, higher score) should get 0.03
    # The second one (E2) should be capped at 0.02

    e1_alloc = next(a for a in allocations if a.event_id == "E1")
    e2_alloc = next(a for a in allocations if a.event_id == "E2")

    assert e1_alloc.allocated_stake_fraction == pytest.approx(0.03)
    assert e2_alloc.allocated_stake_fraction == pytest.approx(0.02)
    assert e2_alloc.allocation_status.value == "reduced_by_budget"

def test_correlation_guard():
    config = PortfolioConfig(
        default_allocation_strategy="sequential_cap",
        same_event_related_market_guard=True
    )
    runner = PortfolioRunner(config)

    dt = datetime.datetime.utcnow()
    candidates = [
        PortfolioCandidateRecord(
            event_id="E1",
            event_datetime_utc=dt,
            sport="football",
            market_type="1x2",
            action_class="approved_candidate",
            selected_side="home",
            proposed_stake_fraction=0.02,
            proposed_stake_units=20.0,
            bankroll_before_window=1000.0,
            signal_score=0.9
        ),
        PortfolioCandidateRecord(
            event_id="E1", # Same event!
            event_datetime_utc=dt,
            sport="football",
            market_type="ou_2_5", # Different market
            action_class="approved_candidate",
            selected_side="over",
            proposed_stake_fraction=0.02,
            proposed_stake_units=20.0,
            bankroll_before_window=1000.0,
            signal_score=0.8
        )
    ]

    allocations, manifest = runner.allocate(candidates)

    assert len(allocations) == 2
    # Second one should be skipped
    skipped = [a for a in allocations if a.allocation_status.value == "skipped_by_correlation_guard"]
    assert len(skipped) == 1
    assert skipped[0].market_type == "ou_2_5"
